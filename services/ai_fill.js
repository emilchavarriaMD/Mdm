/* Llena el formulario de ActivityInfo. NUNCA pulsa Guardar registro ni Guardar como borrador. */
(function () {
  if (window.__mdm) return;
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const norm = (s) => (s || "").replace(/\s+/g, " ").replace(/\*/g, "").replace(/OBLIGATORIO/g, "").trim().toLowerCase();
  const plain = (s) => norm(s).normalize("NFD").replace(/[\u0300-\u036f]/g, "");   // sin tildes ni mayúsculas
  const visible = (e) => e && e.getBoundingClientRect().height > 0;
  const FORBIDDEN = /guardar|save|est[aá] hecho|cancelar/i;   // jamás se hace clic en nada que guarde, cierre o cancele

  function findLabel(text, within) {
    const t = norm(text);
    const root = within || document;
    const labels = [...root.querySelectorAll("label")];
    let hit = labels.find((l) => norm(l.childNodes.length ? [...l.childNodes].filter((n) => n.nodeType === 3 || (n.nodeType === 1 && n.tagName !== "INPUT" && !n.querySelector("input"))).map((n) => n.textContent).join(" ") : l.textContent) === t);
    if (!hit) hit = labels.find((l) => norm(l.textContent).startsWith(t));
    return hit || null;
  }
  function inputFor(label) {
    if (label.querySelector("input")) return label.querySelector("input");
    const box = label.closest(".forminput__field") || label.parentElement;
    return box.querySelector("input[type=text], input:not([type]), textarea");
  }
  function setNative(input, value) {
    const proto = input.tagName === "TEXTAREA" ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
    Object.getOwnPropertyDescriptor(proto, "value").set.call(input, value);
    input.dispatchEvent(new Event("input", { bubbles: true }));
  }
  function click(el) {
    const b = el.closest && el.closest("button");
    if (b && FORBIDDEN.test(b.innerText || "")) throw new Error("Bloqueado: este programa nunca guarda ni cierra el registro");
    ["pointerdown", "mousedown", "pointerup", "mouseup", "click"].forEach((t) =>
      el.dispatchEvent(new MouseEvent(t, { bubbles: true, cancelable: true, view: window })));
  }
  async function waitFor(fn, ms = 4000) {
    const t0 = Date.now();
    while (Date.now() - t0 < ms) { const v = fn(); if (v) return v; await sleep(80); }
    return null;
  }
  async function setText(label, value) {
    const l = findLabel(label); if (!l) throw new Error("No encontré el campo: " + label);
    const inp = inputFor(l); if (!inp) throw new Error("Campo sin cuadro de texto: " + label);
    inp.scrollIntoView({ block: "center" }); inp.focus(); setNative(inp, String(value));
    inp.dispatchEvent(new Event("change", { bubbles: true })); inp.blur();
  }
  async function setLookup(label, value, within) {
    const l = findLabel(label, within); if (!l) throw new Error("No encontré el campo: " + label);
    const inp = inputFor(l); if (!inp) throw new Error("Lista sin cuadro: " + label);
    inp.scrollIntoView({ block: "center" }); inp.focus(); click(inp);
    setNative(inp, String(value));
    const want = plain(value);
    const item = await waitFor(() => {
      const items = [...document.querySelectorAll(".listpicker__item")].filter(visible);
      return items.find((i) => plain(i.innerText) === want) || items.find((i) => plain(i.innerText).includes(want));
    });
    if (!item) throw new Error(`No hay opción «${value}» en «${label}»`);
    click(item); await sleep(250);
    return item.innerText.trim();
  }
  async function setRadio(label, option) {
    const l = findLabel(label); if (!l) throw new Error("No encontré el grupo: " + label);
    const box = l.closest(".forminput__field") || l.parentElement;
    const want = norm(option);
    const cand = [...box.querySelectorAll("label, div, span")].filter((e) => visible(e) && norm(e.textContent) === want);
    if (!cand.length) throw new Error(`No hay opción «${option}» en «${label}»`);
    const el = cand[cand.length - 1]; el.scrollIntoView({ block: "center" });
    click(el.closest("label") || el); await sleep(200);
  }
  // Casillas de varias opciones: marca solo las que faltan (nunca desmarca).
  async function setChecks(label, options) {
    const l = findLabel(label); if (!l) throw new Error("No encontré el grupo: " + label);
    const box = l.closest(".forminput__field") || l.parentElement;
    for (const opt of options) {
      const want = norm(opt);
      const lab = [...box.querySelectorAll("label")].find((x) => x.querySelector("input[type=checkbox]") && norm(x.textContent) === want);
      if (!lab) throw new Error(`No hay opción «${opt}» en «${label}»`);
      if (lab.querySelector("input").checked) continue;
      lab.scrollIntoView({ block: "center" }); click(lab); await sleep(300);
    }
  }
  // Lista, texto o grupo de opciones: detecta qué es el campo.
  async function setAuto(label, value) {
    const l = findLabel(label); if (!l) throw new Error("No encontré el campo: " + label);
    const box = l.closest(".forminput__field") || l.parentElement;
    if (box.querySelector('[role="radio"], [role="checkbox"]')) return setRadio(label, value);
    // Si es una lista desplegable, solo se acepta una opción de la lista (si no, queda en rojo): no se escribe texto libre.
    if (box.querySelector(".field__trigger, label.forminput__lookup__key")) return setLookup(label, value);
    try { return await setLookup(label, value); } catch (e) { return setText(label, value); }
  }
  async function step(log, name, fn) { try { await fn(); } catch (e) { log.push(name + ": " + e.message); } }

  // Ficha de atención integral (página principal). No guarda: la ficha la crea la persona a mano.
  async function fillFicha(d) {
    const log = [];
    const S = (n, f) => step(log, n, f);
    const val = (label) => { const l = findLabel(label); const i = l && inputFor(l); return i ? plain(i.value) : ""; };
    // Lookup que solo se toca si todavía no tiene ese valor (ActivityInfo a veces ya lo trae puesto).
    const lk = (label, v) => (val(label) === plain(v) ? Promise.resolve() : setLookup(label, v));
    // El formulario es dependiente: se llena en el orden en que va apareciendo y se espera a que salgan los campos nuevos.
    // 1) Punto de atención (al elegir el lugar se llenan País y Departamento y aparecen campos nuevos, como el pueblo)
    if (d.lugar) {
      await S("Lugar de atención", () => lk("Puntos de atención sanitaria", d.lugar));
      await waitFor(() => val("Centroamérica País"), 4000); await sleep(600);
    }
    // 2) Proyecto
    if (d.donante) { await S("Proyecto: Donante", () => lk("Donante Nombre", d.donante)); await sleep(500); }
    if (d.proyecto) { await S("Proyecto: Título", () => lk("PROYECTOS Título del proyecto", d.proyecto)); await sleep(500); }
    if (d.perfin) await S("Proyecto: PERFIN", () => lk("PROYECTOS PERFIN", d.perfin));
    // 3) Datos de la persona, en el orden de la página
    if (d.fecha) await S("Fecha consulta", () => setText("Fecha consulta", d.fecha));
    if (d.genero) await S("Género", () => setRadio("Género", d.genero));
    if (d.lgtbiq) await S("¿Se identifica como persona LGTBIQ+?", () => setLookup("¿Se identifica como persona LGTBIQ+?", d.lgtbiq));
    if (d.pueblo) {
      await waitFor(() => findLabel("¿Con qué pueblo se identifica la persona atendida?"), 4000);
      await S("Pueblo con el que se identifica", () => setAuto("¿Con qué pueblo se identifica la persona atendida?", d.pueblo));
    }
    if (d.nacionalidad) await S("País de nacionalidad", () => setLookup("País de Nacionalidad", d.nacionalidad));
    if (d.idioma) await S("Idioma", () => setLookup("Idioma", d.idioma));
    if (d.nombres) await S("Nombre", () => setText("Nombre", d.nombres));
    if (d.apellidos) await S("Apellidos", () => setText("Apellidos", d.apellidos));
    if (d.tiene_fecha_nac) {
      await S("Fecha de nacimiento SI/NO", () => setRadio("Fecha de nacimiento SI/NO", d.tiene_fecha_nac));
      if (d.tiene_fecha_nac === "No" && d.edad) {
        await waitFor(() => findLabel("Años (manual)"), 5000);
        await S("Años (manual)", () => setText("Años (manual)", d.edad));
      }
      if (d.tiene_fecha_nac === "Si" && d.fecha_nac) {
        await sleep(400);
        await S("Fecha de nacimiento", () => setText("Fecha de nacimiento", d.fecha_nac));
      }
    }
    if (d.estado_civil) await S("Estado civil", () => setRadio("Estado civil", d.estado_civil));
    if (d.escolaridad) await S("Grado de escolaridad", () => setRadio("Grado de escolaridad", d.escolaridad));
    if (d.ocupacion) await S("Sector de ocupación", () => setAuto("Sector de ocupación", d.ocupacion));
    if (d.discapacidad) await S("Discapacidad", () => setRadio("¿Tiene algún tipo de discapacidad?", d.discapacidad));
    if (d.perfil) await S("Perfil de población", () => setAuto("Perfil de población", d.perfil));
    if (d.derivado) await S("¿Ha sido derivado/a?", () => setRadio("¿Ha sido derivado/a?", d.derivado));
    if ((d.consultas || []).length) await S("Consulta a realizar", () => setChecks("Consulta a realizar", d.consultas));
    return log;
  }

  // Subformulario de Atención Primaria de Salud (se abre con su botón; no se pulsa «Está hecho»).
  async function openAps() {
    const b = await waitFor(() => [...document.querySelectorAll("button")].find((x) => /Nuevo registro en Atención primaria de salud/i.test(x.innerText)), 5000);
    if (!b) throw new Error("No encontré el botón del subformulario de Atención primaria");
    b.scrollIntoView({ block: "center" });
    ["pointerdown", "mousedown", "pointerup", "mouseup", "click"].forEach((t) => b.dispatchEvent(new MouseEvent(t, { bubbles: true, cancelable: true, view: window })));
    await waitFor(() => findLabel("Profesional que atiende"), 6000);
    await sleep(500);
  }
  async function fillAps(d) {
    const log = [];
    const S = (n, f) => step(log, n, f);
    try { await openAps(); } catch (e) { return ["Subformulario APS: " + e.message]; }
    if (d.profesional) {
      await S("Profesional que atiende", () => {
        const g = findLabel("Profesional que atiende");
        return setLookup("Nombre y Apellidos", d.profesional, g && (g.closest(".forminput__field") || g.parentElement));
      });
      await sleep(900);  // al elegirla se llenan País, Ciudad y Profesión
    }
    await S("¿Mismo punto de atención?", () => setRadio("¿Mismo punto de atención registrado en la ficha integral?", "Sí"));
    await S("¿Mismo proyecto?", () => setRadio("¿Mismo proyecto registrado en la ficha integral?", "Sí"));
    if (d.tipo_consulta) await S("Tipo de consulta", () => setRadio("Tipo de consulta", d.tipo_consulta));
    if (d.n_dx) await S("¿Cuántos diagnósticos?", () => setText("¿Cuántos diagnósticos?", String(d.n_dx)));
    return log;
  }
  async function run(d) {
    const falla = await fillFicha(d);
    const aps = (d.consultas || []).includes("Atención Primaria de Salud") ? await fillAps(d) : [];
    return { ficha: falla, aps: aps };
  }
  window.__mdm = { findLabel, setText, setLookup, setRadio, setChecks, setAuto, fillFicha, fillAps, run, sleep, version: 5 };
})();

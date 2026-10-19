/* Llena el formulario de ActivityInfo. NUNCA pulsa Guardar registro ni Guardar como borrador. */
(function () {
  const VERSION = 13;
  if (window.__mdm && window.__mdm.version === VERSION) return;   // una versión vieja en la pestaña se reemplaza
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
    const want = plain(value);
    const shown = () => [...document.querySelectorAll(".listpicker__item")].filter(visible);
    // Las listas grandes (como los puntos de atención) tardan en cargar la primera vez: se reescribe el texto
    // cada pocos segundos y se espera la opción EXACTA; solo si no existe se acepta la más parecida.
    let item = null;
    const t0 = Date.now();
    let nudge = 0;
    while (Date.now() - t0 < 45000 && !item) {
      if (Date.now() - t0 >= nudge) { setNative(inp, ""); await sleep(150); setNative(inp, nudge > 7000 ? String(value).slice(0, Math.max(4, Math.ceil(String(value).length / 2))) : String(value)); nudge += 3500; }
      await sleep(250);
      const items = shown();
      item = items.find((i) => plain(i.innerText) === want) || null;
      if (!item && Date.now() - t0 > 25000) {
        const near = items.filter((i) => plain(i.innerText).includes(want)).sort((x, y) => x.innerText.length - y.innerText.length);
        item = near[0] || null;
      }
    }
    if (!item) throw new Error(`No hay opción «${value}» en «${label}»`);
    click(item); await sleep(400);
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
    // Con un lugar «… - Otro» aparece «Especifique punto de atención» (justo debajo, antes del proyecto)
    if (d.punto_especifico) {
      await S("Especifique punto de atención", async () => {
        const ok = await waitFor(() => findLabel("Especifique punto de atención"), 4000);
        if (!ok) throw new Error("no apareció el campo (solo sale si el lugar de atención es «… - Otro»)");
        await setText("Especifique punto de atención", d.punto_especifico);
      });
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
  // Diagnósticos del subformulario APS: «Diagnóstico APS», «Diagnóstico APS 2», «3». Cada uno tiene dos listas
  // (descripción de la morbilidad CIE-11 y código); al elegir una, ActivityInfo llena la otra.
  function input_focus(el) { el.scrollIntoView({ block: "center" }); el.focus(); }
  async function fillDx(d, log, info) {
    const dxs = d.dx || [];
    for (let i = 0; i < dxs.length && i < 3; i++) {
      const dx = dxs[i];
      const nombre = i === 0 ? "Diagnóstico APS" : "Diagnóstico APS " + (i + 1);
      const tag = `Diagnóstico ${i + 1} (${dx.abrev})`;
      try {
        const h = await waitFor(() => [...document.querySelectorAll("h4")].find((x) => norm(x.textContent) === norm(nombre)), 6000);
        if (!h) throw new Error("no apareció el campo " + nombre);
        const box = h.closest(".forminput__field");
        const keys = [...box.querySelectorAll("label.forminput__lookup__key")];
        const inD = keys[0] && keys[0].querySelector("input"), inC = keys[1] && keys[1].querySelector("input");
        if (!inD || !inC) throw new Error("no encontré las listas de descripción y código");
        let elegido = null;
        const probar = async (input, texto, esCodigo) => {
          input.scrollIntoView({ block: "center" }); input.focus(); click(input);
          setNative(input, ""); await sleep(150); setNative(input, texto);
          const want = plain(texto);
          // Nunca se elige una opción que no se parezca a lo buscado (un diagnóstico equivocado es peor que ninguno).
          const it = await waitFor(() => {
            const items = [...document.querySelectorAll(".listpicker__item")].filter(visible);
            if (esCodigo) return items.find((x) => plain(x.innerText) === want) || items.find((x) => plain(x.innerText).startsWith(want)) || null;
            return items.find((x) => plain(x.innerText) === want) || items.find((x) => plain(x.innerText).startsWith(want)) || items.find((x) => plain(x.innerText).includes(want)) || null;
          }, 5000);
          if (!it) { setNative(input, ""); input.blur(); return null; }
          const txt = it.innerText.trim(); click(it); await sleep(900); return txt;
        };
        // La descripción viene de la lista del propio formulario: se elige por ella y ActivityInfo pone el código.
        const texto = dx.descripcion || dx.abrev;
        if (texto) elegido = await probar(inD, texto, false);
        if (!elegido && texto) {
          // Plan B: abrir la lista completa (sin escribir) y tomar solo la opción idéntica.
          const want = plain(texto);
          setNative(inD, ""); input_focus(inD);
          const trig = inD.closest("label").querySelector(".field__trigger");
          if (trig) click(trig);
          const it = await waitFor(() => [...document.querySelectorAll(".listpicker__item")].filter(visible).find((x) => plain(x.innerText) === want) || null, 4000);
          if (it) { elegido = it.innerText.trim(); it.scrollIntoView({ block: "center" }); click(it); await sleep(900); }
        }
        if (!elegido) throw new Error("no encontré «" + texto + "» en la lista de ActivityInfo; elíjalo a mano");
        const code = inC.value.trim();
        info.push(`${dx.abrev}: «${inD.value.trim()}» ${code}` + (dx.cie11 && code && plain(dx.cie11) !== plain(code) ? ` — el programa tenía ${dx.cie11}, revise` : ""));
      } catch (e) { log.push(tag + ": " + e.message); }
    }
  }
  async function fillAps(d, info) {
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
    if (d.hea && d.tipo_consulta) {
      // El cuadro «Historia de la enfermedad actual» aparece al elegir el tipo de consulta (no con «Tamizaje»).
      await S("Historia de la enfermedad actual", async () => {
        const ok = await waitFor(() => findLabel("Historia de la enfermedad actual"), 5000);
        if (!ok) throw new Error("no apareció el cuadro (con «Tamizaje de signos vitales» no existe)");
        await setText("Historia de la enfermedad actual", d.hea);
      });
    }
    // Signos vitales (después de la HEA y antes de los diagnósticos); solo se escribe lo que no está vacío.
    const vit = [["Sistólica (mayor)", d.sistolica], ["Diastólica (menor)", d.diastolica],
                 ["Frecuencia Cardiaca o Pulso", d.fc], ["Frecuencia Respiratoria", d.fr], ["Temperatura", d.temperatura]];
    if (vit.some((x) => x[1]) && d.tipo_consulta) await waitFor(() => findLabel("Sistólica (mayor)"), 5000);
    for (const [nombre, valor] of vit) {
      if (valor) await S(nombre, () => setText(nombre, String(valor)));
    }
    if (d.n_dx) {
      await S("¿Cuántos diagnósticos?", () => setText("¿Cuántos diagnósticos?", String(d.n_dx)));
      await sleep(900);
      await fillDx(d, log, info);
    }
    return log;
  }
  async function run(d) {
    const falla = await fillFicha(d);
    const info = [];
    const aps = (d.consultas || []).includes("Atención Primaria de Salud") ? await fillAps(d, info) : [];
    return { ficha: falla, aps: aps, info: info };
  }
  window.__mdm = { findLabel, setText, setLookup, setRadio, setChecks, setAuto, fillFicha, fillAps, run, sleep, version: VERSION };
})();

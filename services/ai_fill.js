/* Llena el formulario de ActivityInfo. NUNCA pulsa Guardar registro ni Guardar como borrador. */
(function () {
  const VERSION = 30;
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
    if (!/fecha/i.test(label)) CHK.push({ label, el: inp, esperado: String(value) });
  }
  // «Fecha consulta»: el último campo visible con ese nombre (la ficha principal y cada subformulario tienen el suyo, y el
  // subformulario es lo último que se abrió). FECHAS guarda lo que quedó escrito en cada uno, para informarlo al terminar.
  const FECHAS = {};
  const campoFecha = () => {
    const ls = [...document.querySelectorAll("label")].filter((l) => visible(l) && norm(l.textContent).startsWith("fecha consulta"));
    const l = ls[ls.length - 1];
    return l ? inputFor(l) : null;
  };
  const leerFecha = () => { const i = campoFecha(); return i ? i.value : ""; };
  // Verificación: vuelve a leer lo escrito en los cuadros de texto y avisa si quedó vacío o distinto.
  const CHK = [];
  const compacto = (t) => plain(t).replace(/[^a-z0-9]+/g, "");
  function verificar() {
    const malos = [];
    for (const c of CHK.splice(0)) {
      if (!c.el.isConnected) continue;       // el subformulario ya se cerró: se revisó antes de cerrarlo
      const v = compacto(c.el.value), e = compacto(c.esperado);
      if (v === e) continue;
      malos.push(v ? `«${c.label}» quedó distinto de lo previsto; revíselo` : `«${c.label}» quedó vacío; escríbalo a mano`);
    }
    return malos;
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
    if (box.querySelector('input[type=checkbox]') && !box.querySelector('[role="radio"], input[type=radio]')) return setChecks(label, [value]);
    if (box.querySelector('[role="radio"], [role="checkbox"], input[type=radio]')) return setRadio(label, value);
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
        if (!ok) return;  // la localidad del ATA va aquí solo si el lugar es «… - Otro»; si no sale el campo, se omite
        await setText("Especifique punto de atención", d.punto_especifico);
      });
    }
    // 2) Proyecto
    if (d.donante) { await S("Proyecto: Donante", () => lk("Donante Nombre", d.donante)); await sleep(500); }
    if (d.proyecto) { await S("Proyecto: Título", () => lk("PROYECTOS Título del proyecto", d.proyecto)); await sleep(500); }
    if (d.perfin) await S("Proyecto: PERFIN", () => lk("PROYECTOS PERFIN", d.perfin));
    // 3) Datos de la persona, en el orden de la página
    if (d.fecha) await S("Fecha consulta", () => setText("Fecha consulta", d.fecha));
    else log.push(`Fecha consulta: el ATA no trae fecha; en ActivityInfo quedó la de HOY (${leerFecha() || "?"}). Corríjala a mano.`);
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
    if (d.telefono) await S("Número de teléfono", () => setText("Número de teléfono", d.telefono));
    if (d.discapacidad) await S("Discapacidad", () => setRadio("¿Tiene algún tipo de discapacidad?", d.discapacidad));
    if (d.discapacidad === "Sí" && (d.discapacidad_tipo || []).length) {   // al responder «Sí» aparece «¿Qué tipo de discapacidad?»
      await S("Tipo de discapacidad", async () => {
        const ok = await waitFor(() => findLabel("¿Qué tipo de discapacidad?"), 4000);
        if (!ok) throw new Error("no apareció «¿Qué tipo de discapacidad?»");
        await setChecks("¿Qué tipo de discapacidad?", d.discapacidad_tipo);
      });
    }
    if (d.perfil) await S("Perfil de población", () => setAuto("Perfil de población", d.perfil));
    if (d.derivado) await S("¿Ha sido derivado/a?", () => setRadio("¿Ha sido derivado/a?", d.derivado));
    // Derivación (desde): con «Sí» aparecen Procedencia, Observaciones y Código de referencia (en ese orden)
    if (d.derivado === "Sí" && (d.derivado_procedencia || d.derivado_obs || d.derivado_codigo)) {
      await sleep(600);
      const tras = (desde, texto) => {          // la primera etiqueta «texto» que viene después de «desde»
        const ls = [...document.querySelectorAll("label")];
        const i = ls.findIndex((l) => norm(l.textContent).startsWith(norm(desde)));
        return i < 0 ? null : ls.slice(i + 1).find((l) => norm(l.textContent).startsWith(norm(texto))) || null;
      };
      const poner = async (nombre, desde, texto, valor) => {
        const l = tras(desde, texto); if (!l) throw new Error("No encontré el campo: " + nombre);
        const inp = inputFor(l); if (!inp) throw new Error("Campo sin cuadro de texto: " + nombre);
        inp.scrollIntoView({ block: "center" }); inp.focus(); setNative(inp, String(valor));
        inp.dispatchEvent(new Event("change", { bubbles: true })); inp.blur();
        CHK.push({ label: nombre, el: inp, esperado: String(valor) });
      };
      if (d.derivado_procedencia) await S("Procedencia de la derivación", async () => {
        const ok = await waitFor(() => findLabel("Procedencia de la derivación"), 4000);
        if (!ok) throw new Error("no apareció (solo sale si «¿Ha sido derivado/a?» es Sí)");
        await setAuto("Procedencia de la derivación", d.derivado_procedencia);
      });
      if (d.derivado_obs) await S("Derivación: Observaciones", () => poner("Derivación: Observaciones", "Procedencia de la derivación", "Observaciones", d.derivado_obs));
      if (d.derivado_codigo) await S("Código de referencia", () => poner("Código de referencia", "Procedencia de la derivación", "Código de referencia", d.derivado_codigo));
    }
    if ((d.consultas || []).length) await S("Consulta a realizar", () => setChecks("Consulta a realizar", d.consultas));
    // La ficha principal también propone la fecha de HOY: al terminar se comprueba que sigue siendo la del ATA.
    await sleep(400);
    FECHAS.ficha = leerFecha();
    if (d.fecha && FECHAS.ficha !== String(d.fecha)) log.push(`Fecha consulta: quedó «${FECHAS.ficha}» en vez de «${d.fecha}» (la fecha del ATA); corríjala a mano`);
    return log;
  }

  // Subformulario de Atención Primaria de Salud (se abre con su botón; no se pulsa «Está hecho»).
  async function openSub(boton, nombre) {
    const b = await waitFor(() => [...document.querySelectorAll("button")].find((x) => boton.test(x.innerText)), 6000);
    if (!b) throw new Error("No encontré el botón del subformulario de " + nombre);
    b.scrollIntoView({ block: "center" });
    ["pointerdown", "mousedown", "pointerup", "mouseup", "click"].forEach((t) => b.dispatchEvent(new MouseEvent(t, { bubbles: true, cancelable: true, view: window })));
    await waitFor(() => findLabel("Profesional que atiende"), 6000);
    await sleep(500);
  }
  // Cada subformulario (APS y SSR) trae su PROPIA «Fecha consulta», que ActivityInfo propone con la fecha de HOY. La fecha
  // de la consulta es la del ATA, así que se escribe en cada uno y se comprueba que se quedó (por si el formulario vuelve a
  // poner la de hoy). Se toma el último «Fecha consulta» visible: el subformulario es lo último que se abrió.
  async function fijarFecha(d, nombre, log) {
    const clave = nombre.toLowerCase();
    if (!d.fecha) {
      await sleep(300); FECHAS[clave] = leerFecha();
      log.push(`${nombre}: Fecha consulta: el ATA no trae fecha; quedó la de HOY (${FECHAS[clave] || "?"}). Corríjala a mano.`);
      return;
    }
    const f = String(d.fecha);
    await step(log, nombre + ": Fecha consulta", async () => {
      const poner = () => {
        const inp = campoFecha(); if (!inp) throw new Error("no encontré el campo");
        if (inp.value === f) return;
        inp.scrollIntoView({ block: "center" }); inp.focus(); setNative(inp, f);
        inp.dispatchEvent(new Event("change", { bubbles: true })); inp.blur();
      };
      poner(); await sleep(600); poner(); await sleep(300);
      FECHAS[clave] = leerFecha();
      if (FECHAS[clave] !== f) throw new Error(`quedó «${FECHAS[clave]}» en vez de «${f}» (la fecha del ATA); corríjala a mano`);
    });
  }
  const openAps = () => openSub(/Nuevo registro en Atención primaria de salud/i, "Atención primaria");
  const openSsr = () => openSub(/Nuevo registro en Salud Sexual y Reproductiva/i, "Salud Sexual y Reproductiva");
  // ÚNICO lugar donde se pulsa «Está hecho»: el de Atención primaria, y solo si hay que seguir con SSR y la persona lo
  // permitió. «Está hecho» solo devuelve a la ficha (nada se crea ni se guarda). Se busca por el texto EXACTO.
  async function terminarAps() {
    const b = [...document.querySelectorAll("button")].filter(visible).find((x) => norm(x.innerText) === "está hecho");
    if (!b) throw new Error("no encontré «Está hecho» en el subformulario de Atención primaria");
    b.scrollIntoView({ block: "center" });
    ["pointerdown", "mousedown", "pointerup", "mouseup", "click"].forEach((t) => b.dispatchEvent(new MouseEvent(t, { bubbles: true, cancelable: true, view: window })));
    const ssrBtn = () => [...document.querySelectorAll("button")].some((x) => /Nuevo registro en Salud Sexual y Reproductiva/i.test(x.innerText) && visible(x));
    const apsAbierto = () => { const l = findLabel("Historia de la enfermedad actual"); return !!(l && visible(l)); };
    const ok = await waitFor(() => ssrBtn() && !apsAbierto(), 12000);
    if (!ok) throw new Error("«Está hecho» no cerró el subformulario de Atención primaria (revise los campos obligatorios que falten)");
    await sleep(600);
  }
  // Diagnósticos del subformulario APS: «Diagnóstico APS», «Diagnóstico APS 2», «3». Cada uno tiene dos listas
  // (descripción de la morbilidad CIE-11 y código); al elegir una, ActivityInfo llena la otra.
  function input_focus(el) { el.scrollIntoView({ block: "center" }); el.focus(); }
  async function fillDx(dxs, base, log, info) {
    dxs = dxs || [];
    for (let i = 0; i < dxs.length && i < 3; i++) {
      const dx = dxs[i];
      const nombre = i === 0 ? base : base + " " + (i + 1);
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
    await fijarFecha(d, "APS", log);
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
    // Examen físico: peso (se escribe a mano en la ventana; la talla nunca se toca y el IMC lo calcula el formulario)
    if (d.peso) await S("Peso", () => setText("Peso", String(d.peso)));
    if (d.examen_fisico) await S("Examen Físico", () => setText("Examen Físico", d.examen_fisico));
    if (d.n_dx) {
      await S("¿Cuántos diagnósticos?", () => setText("¿Cuántos diagnósticos?", String(d.n_dx)));
      await sleep(900);
      await fillDx(d.dx, "Diagnóstico APS", log, info);
    }
    // Plan, derivación y servicio brindado (en el orden de la página). «Servicio brindado» solo aparece con
    // «¿Va a ser derivado?» = Sí; al elegir «Salud» aparece el grupo «Salud».
    if (d.plan) await S("Plan", () => setText("Plan", d.plan));
    if (d.va_derivado) { await S("¿Va a ser derivado?", () => setAuto("¿Va a ser derivado?", d.va_derivado)); await sleep(700); }
    if (d.n_servicios) await S("¿A cuántos servicios se deriva?", () => setAuto("¿A cuántos servicios se deriva?", d.n_servicios));
    if (d.transfronteriza) await S("¿Referencia Transfronteriza?", () => setAuto("¿Referencia Transfronteriza?", d.transfronteriza));
    if (d.servicio_brindado) {
      await S("Servicio brindado", async () => {
        const ok = await waitFor(() => findLabel("Servicio brindado"), 5000);
        if (!ok) throw new Error("no apareció (solo sale si «¿Va a ser derivado?» es Sí)");
        await setRadio("Servicio brindado", d.servicio_brindado);
      });
      await sleep(600);
    }
    if (d.servicio_salud && d.servicio_brindado === "Salud") {
      // «Salud» también es una opción de «Servicio brindado»: el grupo se busca por su título (h4), no por la etiqueta.
      await S("Servicio brindado: Salud", async () => {
        const hbox = () => { const h = [...document.querySelectorAll("h4")].find((x) => norm(x.textContent) === "salud"); return h && h.closest(".forminput__field"); };
        const box = await waitFor(hbox, 5000);
        if (!box) throw new Error("no apareció el grupo «Salud»");
        const want = norm(d.servicio_salud);
        const cand = [...box.querySelectorAll("label, div, span")].filter((e) => visible(e) && norm(e.textContent) === want);
        if (!cand.length) throw new Error(`no hay la opción «${d.servicio_salud}»`);
        const el = cand[cand.length - 1]; el.scrollIntoView({ block: "center" }); click(el.closest("label") || el); await sleep(200);
      });
    }
    return log;
  }
  // Subformulario de Salud Sexual y Reproductiva (en el orden de la página). No pulsa «Está hecho» ni guarda.
  async function fillSsr(d, info) {
    const log = [];
    const S = (n, f) => step(log, n, f);
    const x = d.ssr || {};
    try { await openSsr(); } catch (e) { return ["Subformulario SSR: " + e.message]; }
    await fijarFecha(d, "SSR", log);
    if (d.profesional) {
      await S("SSR: Profesional que atiende", () => {
        const g = findLabel("Profesional que atiende");
        return setLookup("Nombre y Apellidos", d.profesional, g && (g.closest(".forminput__field") || g.parentElement));
      });
      await sleep(900);
    }
    if (x.mismo_punto) await S("SSR: ¿Mismo punto de atención?", () => setRadio("¿Mismo punto de atención registrado en la ficha integral?", x.mismo_punto));
    if (x.mismo_proy) await S("SSR: ¿Mismo proyecto?", () => setRadio("¿Mismo proyecto registrado en la ficha integral?", x.mismo_proy));
    if (x.tipo) await S("SSR: Tipo de consulta", () => setRadio("Tipo de consulta", x.tipo));
    if (x.ficha) await S("SSR: ¿Ficha corta o larga?", () => setRadio("¿Ficha corta o larga?", x.ficha));
    if (x.recibio_aps) {
      // solo existe si en la ficha también se marcó Atención primaria
      const l = await waitFor(() => findLabel("¿Recibió APS el mismo día"), 2500);
      if (l) await S("SSR: ¿Recibió APS el mismo día?", () => setAuto("¿Recibió APS el mismo día", x.recibio_aps));
      else log.push("SSR: ¿Recibió APS el mismo día?: no apareció (solo sale si también se marcó Atención primaria)");
    }
    if (x.violencia) {
      await S("SSR: ¿Ha sufrido violencia?", () => setAuto("¿Ha sufrido violencia?", x.violencia));
      await sleep(600);
      if (x.viol_genero) await S("SSR: Violencia de género", () => setAuto("Violencia de género", x.viol_genero));
      if (x.viol_otras) await S("SSR: Otras situaciones de violencia", () => setAuto("Otras Situaciones de Violencia", x.viol_otras));
    }
    const hea = x.hea !== undefined ? x.hea : d.hea;
    if (hea) {
      await S("SSR: Historia de la enfermedad actual", async () => {
        const ok = await waitFor(() => findLabel("Historia de la enfermedad actual"), 5000);
        if (!ok) throw new Error("no apareció el cuadro");
        await setText("Historia de la enfermedad actual", hea);
      });
    }
    // Antecedentes de ficha larga (según el género): menarquía, ritmo, citología, etc.
    for (const [k, lab, auto] of [["menarquia", "Menarquía", false], ["espermarquia", "Espermarquia", false], ["ritmo", "Ritmo menstrual", false],
         ["trast_mens", "Transtorno Menstrual", true], ["menopausia", "Menopausia", true], ["citologia", "Última citología", false],
         ["prueba_vph", "¿Se ha realizado la prueba de detección de VPH el último año?", true],
         ["autoex_mamas", "¿Se ha realizado autoexamen de mamas en el último mes?", true],
         ["autoex_test", "¿Se ha realizado el autoexamen de testículos en el último mes?", true],
         ["tamizaje_prost", "¿Se ha realizado el tamizaje de próstata en el último año?", true]]) {
      if (x[k]) await S("SSR: " + lab, () => (auto ? setAuto(lab, x[k]) : setText(lab, x[k])));
    }
    // Antecedentes (en el orden de la página). Con «Sí» aparecen campos nuevos.
    if (x.its) {
      await S("SSR: Antecedentes de ITS", () => setAuto("Antecedentes de ITS", x.its));
      if (x.its === "Sí" && x.its_cual) { await sleep(600); await S("SSR: ITS ¿Cuál?", () => setText("¿Cuál?", x.its_cual)); }
    }
    if (x.itu) {
      await S("SSR: Antecedentes de ITU", () => setAuto("Antecedentes de ITU", x.itu));
      if (x.itu === "Sí") {
        await sleep(600);
        if (x.itu_complicada) await S("SSR: ¿ITU complicada?", () => setAuto("¿ITU complicada?", x.itu_complicada));
        if (x.itu_episodios) await S("SSR: Número de episodios de ITU al año", () => setText("Número de episodios de ITU al año", x.itu_episodios));
      }
    }
    // Antecedentes obstétricos (en el orden de la página): con embarazo actual «Sí» aparecen FUM, edad gestacional y control prenatal
    if (x.embarazo_actual) {
      await S("SSR: Embarazo actual", () => setAuto("Embarazo actual", x.embarazo_actual));
      if (x.embarazo_actual === "Sí") {
        await sleep(600);
        if (x.conoce_fum) {
          await S("SSR: ¿Conoce la fecha de la última menstruación?", () => setAuto("¿Conoce la fecha de la última menstruación", x.conoce_fum));
          await sleep(600);
          if (x.fum) await S("SSR: FUM", () => setText("Fecha de la última menstruación", x.fum));
          if (x.eg_manual) await S("SSR: Edad gestacional (manual)", () => setText("Edad Gestacional (manual)", x.eg_manual));
        }
      }
    }
    if (x.embarazo_anterior) {
      await S("SSR: Embarazo anterior", () => setAuto("Embarazo Anterior", x.embarazo_anterior));
      await sleep(600);
      for (const [k, lab] of [["gestaciones", "Gestaciones"], ["partos", "Partos"], ["cesareas", "Cesáreas"], ["abortos", "Abortos"], ["obitos", "Óbitos"], ["hijos_vivos", "Hijos vivos"], ["hijos_muertos", "Hijos muertos"]]) {
        if (x[k]) await S("SSR: " + lab, () => setText(lab, x[k]));
      }
    }
    if (x.embarazo_actual === "Sí" && x.cpn) {
      await S("SSR: ¿Ha tenido control prenatal anterior?", () => setAuto("¿Ha tenido control prenatal anterior?", x.cpn));
      if (x.cpn === "Sí" && x.cpn_lugar) { await sleep(500); await S("SSR: Lugar de control prenatal", () => setText("Lugar de Control Prenatal", x.cpn_lugar)); }
    }
    // «Lactancia Materna» solo existe en la página cuando «Hijos vivos» es 1 o más (y hubo embarazo anterior)
    if (x.lactancia) await S("SSR: Lactancia materna", async () => {
      const ok = await waitFor(() => findLabel("Lactancia Materna"), 3500);
      if (!ok) throw new Error("no apareció: ActivityInfo solo la muestra si «Hijos vivos» es 1 o más; márquela a mano cuando corresponda");
      await setAuto("Lactancia Materna", x.lactancia);
    });
    if ((x.vacunacion || []).length) await S("SSR: Vacunación", () => setChecks("Vacunación", x.vacunacion));
    for (const [k, lab] of [["vph", "VPH"], ["papanicolau", "Papanicolau"], ["examen_mama", "Examen de mama"]]) {
      if (x[k]) await S("SSR: " + lab, () => setAuto(lab, x[k]));
    }
    if (x.observaciones) await S("SSR: Observaciones", () => setText("Observaciones", x.observaciones));
    const exa = x.examen_fisico !== undefined ? x.examen_fisico : d.examen_fisico;
    if (exa) await S("SSR: Exámen físico", () => setText("Exámen físico", exa));
    if (x.n_dx) {
      await S("SSR: Número de diagnósticos", () => setRadio("Número de diagnósticos", String(x.n_dx)));
      await sleep(900);
      await fillDx(x.dx, "Diagnóstico SSR", log, info);
    }
    if (x.obs_dx) await S("SSR: Observaciones Diagnóstico", () => setText("Observaciones Diagnóstico", x.obs_dx));
    // Uso de métodos anticonceptivos: con consejería «Si» aparecen ¿Ya planifica?, método elegido y acceso
    if (x.consejeria) {
      await S("SSR: ¿Ha recibido consejería anticoncepción?", () => setAuto("¿Ha recibido consejería anticoncepción durante esta consulta?", x.consejeria));
      if (x.consejeria === "Si") {
        await sleep(700);
        if (x.ya_planifica) {
          await S("SSR: ¿Ya planifica?", () => setAuto("¿Ya planifica?", x.ya_planifica));
          await sleep(600);
          if (x.ya_planifica === "Sí" && (x.metodos_actuales || []).length) await S("SSR: Método/s actual/es", () => setChecks("Metodo/s anticonceptivo/s actual", x.metodos_actuales));
        }
        // Lista de verificación de embarazo (sale con Mujer CIS / Hombre TRANS), antes del método elegido
        const LVE = [["menstruacion", "1. Menstruación"], ["abstinencia", "2. Abstinencia sexual"],
          ["metodo", "3. Metodo anticonceptvo desde última menstruación"], ["bebe4", "4. Bebé en las últimas 4 semanas"],
          ["bebe6", "5. Bebé de menos de 6 meses"], ["aborto", "6. Aborto en los últimos días"]];
        for (const [k, rot] of LVE) {
          const v = (x.lve || {})[k];
          if (v) await S("SSR: Lista de verificación de embarazo — " + rot, () => setAuto(rot, v));
        }
        if ((x.metodos_elegidos || []).length) { await S("SSR: Método/s elegido/s", () => setChecks("Método/s anticonceptivo/s elegido", x.metodos_elegidos)); await sleep(500); }
        if (x.acceso) await S("SSR: Acceso", () => setAuto("Acceso", x.acceso));
      }
    }
    const plan = x.plan !== undefined ? x.plan : d.plan;
    if (plan) await S("SSR: Plan", () => setText("Plan", plan));
    // Derivación (solo aparece «Servicio brindado» con «¿Va a ser derivado?» = Sí; con «Salud» aparece el grupo «Salud»)
    if (x.va_derivado) { await S("SSR: ¿Va a ser derivado?", () => setAuto("¿Va a ser derivado?", x.va_derivado)); await sleep(700); }
    if (x.transfronteriza) await S("SSR: Referencia Transfronteriza", () => setAuto("Referencia Transfronteriza", x.transfronteriza));
    if (x.servicio_brindado) {
      await S("SSR: Servicio brindado", async () => {
        const ok = await waitFor(() => findLabel("Servicio brindado"), 5000);
        if (!ok) throw new Error("no apareció (solo sale si «¿Va a ser derivado?» es Sí)");
        await setRadio("Servicio brindado", x.servicio_brindado);
      });
      await sleep(600);
    }
    if (x.servicio_salud && x.servicio_brindado === "Salud") {
      await S("SSR: Servicio brindado: Salud", async () => {
        const hbox = () => { const h = [...document.querySelectorAll("h4")].find((e) => norm(e.textContent) === "salud"); return h && h.closest(".forminput__field"); };
        const box = await waitFor(hbox, 5000);
        if (!box) throw new Error("no apareció el grupo «Salud»");
        const want = norm(x.servicio_salud);
        const cand = [...box.querySelectorAll("label, div, span")].filter((e) => visible(e) && norm(e.textContent) === want);
        if (!cand.length) throw new Error(`no hay la opción «${x.servicio_salud}»`);
        const el = cand[cand.length - 1]; el.scrollIntoView({ block: "center" }); click(el.closest("label") || el); await sleep(200);
      });
    }
    if (x.victima_sexual) await S("SSR: ¿Víctima/sobreviviente de violencia sexual reciente?", () => setAuto("¿Victima/sobreviviente de violencia sexual reciente?", x.victima_sexual));
    return log;
  }
  async function run(d) {
    CHK.length = 0;
    Object.keys(FECHAS).forEach((k) => delete FECHAS[k]);
    const falla = await fillFicha(d);
    const verif = verificar();
    const info = [];
    const quiereAps = (d.consultas || []).includes("Atención Primaria de Salud");
    const quiereSsr = (d.consultas || []).includes("Salud Sexual y Reproductiva") && !!d.ssr;
    let aps = [];
    if (quiereAps) { aps = await fillAps(d, info); verif.push(...verificar()); }
    let ssr = [];
    if (quiereSsr) {
      if (quiereAps) {
        if (d.permitir_esta_hecho !== true) ssr = ["SSR: no se llenó: falta el permiso para salir del subformulario de Atención primaria; ábralo y llénelo a mano"];
        else {
          try { await terminarAps(); } catch (e) { ssr = ["SSR: " + e.message]; }
        }
      }
      if (!ssr.length) { ssr = await fillSsr(d, info); verif.push(...verificar()); }
    }
    return { ficha: falla, aps: aps, ssr: ssr, info: info, verif: verif, version: VERSION,
             fechas: Object.assign({ esperada: d.fecha ? String(d.fecha) : "" }, FECHAS) };
  }
  window.__mdm = { fillSsr, openSsr, terminarAps, findLabel, setText, setLookup, setRadio, setChecks, setAuto, fillFicha, fillAps, run, verificar, sleep, version: VERSION };
})();

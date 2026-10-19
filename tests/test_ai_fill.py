"""Prueba services/ai_fill.js contra una réplica local del formulario (tests/mock_activityinfo.html), en Chromium sin
ventana. No usa internet ni ActivityInfo. Se omite si Playwright o Chromium no están instalados (la PC del usuario
no los necesita)."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

try:
    from playwright.sync_api import sync_playwright
except Exception:  # noqa: BLE001
    sync_playwright = None

PAYLOAD = {
    "lugar": "Cortes-otro", "punto_especifico": "Brigada Brisas 1", "donante": "ECHO", "proyecto": "ECHO - COMPASS",
    "perfin": "F09010020", "fecha": "2026-10-19", "genero": "Mujer CIS", "lgtbiq": "No", "pueblo": "Mestizo",
    "nacionalidad": "Honduras", "idioma": "Español", "nombres": "Ana", "apellidos": "Prueba", "tiene_fecha_nac": "No",
    "edad": "34", "estado_civil": "Soltero/a", "escolaridad": "Primaria", "ocupacion": "Estudiante",
    "discapacidad": "No", "perfil": "Persona en riesgo de desplazamiento", "derivado": "No",
    "consultas": ["Atención Primaria de Salud"], "profesional": "Nadia Alejandra Chavarria Lopez",
    "tipo_consulta": "Primera",
    "hea": "Beneficiaria Fem de 34 años de edad, que presenta antecedente de hipertensión arterial esencial.",
    "dx": [{"abrev": "HTA", "descripcion": "Hipertensión esencial, sin especificación", "cie11": "BA00.Z"},
           {"abrev": "Dermatitis", "descripcion": "Dermatitis y eccema, sin especificación", "cie11": "EA8Z"},
           {"abrev": "Inventado", "descripcion": "Diagnóstico que no existe en la lista", "cie11": ""}],
    "sistolica": "120", "diastolica": "70", "fc": "72", "fr": "16", "temperatura": "36.6", "peso": "62", "examen_fisico": "Cefalo-caudal",
    "plan": "Plan", "va_derivado": "Sí", "servicio_brindado": "Salud", "servicio_salud": "MdM - Atención primaria",
    "n_dx": 3,
}

LEER = """() => {
  const v = (sel) => { const e = document.querySelector(sel); return e ? e.value : null; };
  const r = (name) => { const e = document.querySelector(`input[name="${name}"]:checked`); return e ? e.value : null; };
  return {
    lugar: v('#lugar input'), pais: v('#pais input'), especifique: v('#especifique'),
    donante: v('#donante input'), titulo: v('#titulo input'), perfin: v('#perfin input'),
    fecha: v('#fecha'), genero: r('genero'), lgtbiq: v('#lgtbiq input'), pueblo: v('#pueblo input'),
    nac: v('#nac input'), idioma: v('#idioma input'), nombre: v('#nombre'), apellidos: v('#apellidos'),
    fnac: r('fnac'), anios: v('#anios'), civil: r('civil'), escolaridad: r('escolaridad'),
    ocupacion: v('#ocupacion input'), discapacidad: r('discapacidad'), perfil: v('#perfil input'),
    derivado: r('derivado'),
    consultas: [...document.querySelectorAll('#consultas input:checked')].map(x => x.value),
    prof: v('#prof input'), mismo_punto: r('mismo_punto'), mismo_proy: r('mismo_proy'), tipo: r('tipo'),
    hea: v('#hea'), ndx: v('#ndx'),
    sis: v('#sis'), dia: v('#dia'), fc: v('#fc'), fr: v('#fr'), temp: v('#temp'), peso: v('#peso'), talla: v('#talla'), examen: v('#examen'), plan: v('#plan'), vder: v('#derivado_aps input'),
    svc: r('svc'), salud: (document.querySelector('input[name="saludsvc"]:checked') || {}).value || null,
    desc1: v('#desc1 input'), code1: v('#code1 input'), desc2: v('#desc2 input'), code2: v('#code2 input'),
    desc3: v('#desc3 input'),
    saved: window.__saved, clicks: window.__clicks,
    ssr: (() => { const q = (sel) => document.querySelector('#ssr ' + sel);
      const rr = (name) => { const e = document.querySelector(`#ssr input[name="${name}"]:checked`); return e ? e.value : null; };
      if (!document.getElementById('ssr')) return null;
      return { prof: (q('#prof input') || {}).value, mismo_punto: rr('mismo_punto'), mismo_proy: rr('mismo_proy'), tipo: rr('tipo'),
        ficha: rr('ficha'), recibio_aps: (q('#recibio_aps input') || {}).value, hea: q('#hea').value, examen: q('#examen').value, ndx: rr('ndx'),
        desc1: (q('#desc1 input') || {}).value, code1: (q('#code1 input') || {}).value,
        desc2: (q('#desc2 input') || {}).value, code2: (q('#code2 input') || {}).value, plan: q('#plan').value,
        titles: [...document.querySelectorAll('#ssr h4')].map(x => x.textContent),
        violencia: (q('#violencia input') || {}).value, its: rr('its'), itu: rr('itu'), vph: rr('vph'), papa: rr('papa'), mama: rr('mama'),
        vacuna: [...document.querySelectorAll('#ssr #vacuna input:checked')].map(x => x.value), obs: q('#obs').value,
        obsdx: q('#obsdx').value, conse: rr('conse'), sder: (q('#sder input') || {}).value, strans: rr('strans'), ssvc: rr('ssvc'),
        ssalud: rr('ssaludsvc'), victima: rr('victima') }; })(),
    aps_abierto: !!document.getElementById('aps'),
  };
}"""


@unittest.skipIf(sync_playwright is None, "Playwright no está instalado")
class T08_LlenadoSimulado(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pw = sync_playwright().start()
        try:
            cls.browser = cls.pw.chromium.launch()
        except Exception as exc:  # noqa: BLE001
            cls.pw.stop()
            raise unittest.SkipTest(f"Chromium no disponible: {exc}")

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()

    def _run(self, payload):
        page = self.browser.new_page()
        page.goto((ROOT / "tests" / "mock_activityinfo.html").as_uri())
        page.add_script_tag(content=(ROOT / "services" / "ai_fill.js").read_text(encoding="utf-8"))
        rep = page.evaluate("d => window.__mdm.run(d)", payload)
        vals = page.evaluate(LEER)
        page.close()
        return rep, vals

    def test_llena_todo_en_orden_y_nunca_guarda(self):
        rep, v = self._run(PAYLOAD)
        self.assertFalse(v["saved"])
        self.assertNotIn("Guardar registro", v["clicks"])
        self.assertNotIn("Está hecho", v["clicks"])
        self.assertEqual(rep["ficha"], [], rep)
        esperado = {
            "lugar": "Cortes-otro", "pais": "Honduras", "especifique": "Brigada Brisas 1", "donante": "ECHO",
            "titulo": "ECHO - COMPASS", "perfin": "F09010020", "fecha": "2026-10-19", "genero": "Mujer CIS",
            "lgtbiq": "No", "pueblo": "Mestizo", "nac": "Honduras", "idioma": "Español", "nombre": "Ana",
            "apellidos": "Prueba", "fnac": "No", "anios": "34", "civil": "Soltero/a", "escolaridad": "Primaria",
            "ocupacion": "Estudiante", "discapacidad": "No", "perfil": "Persona en riesgo de desplazamiento",
            "derivado": "No", "consultas": ["Atención Primaria de Salud"],
            "prof": "Nadia Alejandra Chavarría López", "mismo_punto": "Sí", "mismo_proy": "Sí", "tipo": "Primera",
            "hea": PAYLOAD["hea"], "ndx": "3",
            "sis": "120", "dia": "70", "fc": "72", "fr": "16", "temp": "36.6", "peso": "62", "talla": "", "examen": "Cefalo-caudal",
            "plan": "Plan", "vder": "Sí", "svc": "Salud", "salud": "MdM - Atención primaria",
            "desc1": "Hipertensión esencial, sin especificación", "code1": "BA00.Z",
            "desc2": "Dermatitis y eccema, sin especificación", "code2": "EA8Z",
        }
        for k, val in esperado.items():
            self.assertEqual(v[k], val, k)
        # el diagnóstico que no existe en la lista NO se reemplaza por otro parecido: queda vacío y se avisa
        self.assertEqual(v["desc3"], "")
        self.assertTrue(any("Inventado" in x for x in rep["aps"]), rep)
        self.assertEqual(len(rep["info"]), 2, rep)

    def _ssr_payload(self, **kw):
        p = dict(PAYLOAD, consultas=["Atención Primaria de Salud", "Salud Sexual y Reproductiva"], permitir_esta_hecho=True,
                 dx=PAYLOAD["dx"][:1], n_dx=1,
                 ssr={"mismo_punto": "Sí", "mismo_proy": "Sí", "tipo": "Primera", "ficha": "Larga", "recibio_aps": "Sí",
                      "dx": [{"abrev": "Vaginosis", "descripcion": "Vaginosis bacteriana", "cie11": "MF3A"},
                             {"abrev": "Cand", "descripcion": "Candidiasis vulvovaginal", "cie11": "1F23.10"}], "n_dx": 2,
                      "violencia": "No", "its": "No", "itu": "Sí", "vph": "No", "papanicolau": "Sí", "examen_mama": "No",
                      "vacunacion": ["Td (toxoide tetánico)", "HEPATITIS B:"], "observaciones": "Obs gral", "obs_dx": "Obs dx",
                      "consejeria": "Si", "va_derivado": "Sí", "transfronteriza": "No", "servicio_brindado": "Salud",
                      "servicio_salud": "MdM-Salud sexual y reproductiva", "victima_sexual": "No"})
        p.update(kw)
        return p

    def test_ssr_se_llena_con_su_propia_lista_y_solo_se_cierra_aps(self):
        rep, v = self._run(self._ssr_payload())
        self.assertEqual(rep["ssr"], [], rep)
        self.assertEqual(rep["ficha"], [], rep)
        self.assertEqual(rep["aps"], [], rep)
        self.assertFalse(v["saved"])
        self.assertEqual(v["clicks"].count("Está hecho"), 1, v["clicks"])      # solo el de APS
        self.assertNotIn("Guardar registro", v["clicks"])
        self.assertNotIn("Guardar como borrador", v["clicks"])
        self.assertFalse(v["aps_abierto"])
        s = v["ssr"]
        self.assertEqual((s["prof"], s["mismo_punto"], s["mismo_proy"], s["tipo"], s["ficha"], s["recibio_aps"]),
                         ("Nadia Alejandra Chavarría López", "Sí", "Sí", "Primera", "Larga", "Sí"))
        self.assertEqual(s["hea"], PAYLOAD["hea"])
        self.assertEqual(s["examen"], "Cefalo-caudal")
        self.assertEqual(s["plan"], "Plan")
        self.assertEqual(s["ndx"], "2")
        self.assertEqual((s["desc1"], s["code1"]), ("Vaginosis bacteriana", "MF3A"))
        self.assertEqual((s["desc2"], s["code2"]), ("Candidiasis vulvovaginal", "1F23.10"))
        self.assertEqual((s["violencia"], s["its"], s["itu"], s["vph"], s["papa"], s["mama"]), ("No", "No", "Sí", "No", "Sí", "No"))
        self.assertEqual(s["vacuna"], ["Td (toxoide tetánico)", "HEPATITIS B:"])
        self.assertEqual((s["obs"], s["obsdx"], s["conse"]), ("Obs gral", "Obs dx", "Si"))
        self.assertEqual((s["sder"], s["strans"], s["ssvc"], s["ssalud"], s["victima"]),
                         ("Sí", "No", "Salud", "MdM-Salud sexual y reproductiva", "No"))

    def test_ssr_sin_permiso_no_pulsa_esta_hecho(self):
        rep, v = self._run(self._ssr_payload(permitir_esta_hecho=False))
        self.assertNotIn("Está hecho", v["clicks"])
        self.assertIsNone(v["ssr"])
        self.assertTrue(rep["ssr"], rep)

    def test_ssr_sin_aps_no_pulsa_nada(self):
        p = self._ssr_payload(consultas=["Salud Sexual y Reproductiva"])
        p["ssr"]["recibio_aps"] = ""
        rep, v = self._run(p)
        self.assertNotIn("Está hecho", v["clicks"])
        self.assertEqual(v["ssr"]["desc1"], "Vaginosis bacteriana")
        self.assertFalse(v["saved"])

    def test_sin_lugar_otro_no_hay_especifique(self):
        p = dict(PAYLOAD, lugar="San Pedro Sula", dx=PAYLOAD["dx"][:1], n_dx=1)
        rep, v = self._run(p)
        self.assertIsNone(v["especifique"])
        self.assertTrue(any("Especifique" in x for x in rep["ficha"]), rep)   # se avisa, no se inventa
        self.assertFalse(v["saved"])

    def test_tamizaje_no_tiene_hea(self):
        p = dict(PAYLOAD, tipo_consulta="Tamizaje de signos vitales", dx=PAYLOAD["dx"][:1], n_dx=1)
        rep, v = self._run(p)
        self.assertIsNone(v["hea"])
        self.assertTrue(any("Historia de la enfermedad actual" in x for x in rep["aps"]), rep)
        self.assertEqual(v["desc1"], "Hipertensión esencial, sin especificación")
        self.assertFalse(v["saved"])


if __name__ == "__main__":
    unittest.main(verbosity=2)

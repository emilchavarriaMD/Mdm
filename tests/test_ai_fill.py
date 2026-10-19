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
    desc1: v('#desc1 input'), code1: v('#code1 input'), desc2: v('#desc2 input'), code2: v('#code2 input'),
    desc3: v('#desc3 input'),
    saved: window.__saved, clicks: window.__clicks,
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
            "desc1": "Hipertensión esencial, sin especificación", "code1": "BA00.Z",
            "desc2": "Dermatitis y eccema, sin especificación", "code2": "EA8Z",
        }
        for k, val in esperado.items():
            self.assertEqual(v[k], val, k)
        # el diagnóstico que no existe en la lista NO se reemplaza por otro parecido: queda vacío y se avisa
        self.assertEqual(v["desc3"], "")
        self.assertTrue(any("Inventado" in x for x in rep["aps"]), rep)
        self.assertEqual(len(rep["info"]), 2, rep)

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

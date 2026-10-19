"""Pruebas del banco de HEA y de la composición con 1-3 diagnósticos (sin interfaz)."""
import random
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services import cie11_catalog as cat  # noqa: E402
from services import hea_banco as hb  # noqa: E402
from services.hea_data import BANK  # noqa: E402


def problemas(t):
    p = []
    if not t.startswith("Benefici"):
        p.append("inicio")
    if "  " in t:
        p.append("doble espacio")
    if ".." in t.replace("...", ""):
        p.append("doble punto")
    if not t.rstrip().endswith((".", "!", "?", '"')):
        p.append("final")
    if re.search(r"\s[,.;]", t):
        p.append("espacio antes de puntuación")
    if re.search(r"\by (i|hi)(?![aeiouáéíóú])", t, re.I):
        p.append("y en vez de e")
    if t.count("Además refiere") > 1:
        p.append("dos veces «Además refiere»")
    if "None" in t:
        p.append("None")
    return p


class T07_HEA(unittest.TestCase):
    def test_banco_completo(self):
        for n, b in BANK.items():
            self.assertIn(b["k"], "CSX", n)
            self.assertTrue(b["t"], n)
            self.assertGreaterEqual(len(b["v"]), 5, n)
            for v in b["v"]:
                self.assertNotIn("___", v, n)
                self.assertFalse(re.match(r"(consulta por|paciente|beneficiari)", v, re.I), (n, v[:40]))

    def test_toda_la_lista_de_activityinfo_tiene_hea(self):
        for d, _c in cat.CATALOG:
            self.assertIsNotNone(hb.bank_id(d), d)

    def test_abreviaturas_del_ata(self):
        for abrev, nombre in (("HTA", "Hipertensión"), ("DM2", "Diabetes"), ("RC", "Nasofaringitis"),
                              ("PF (ACOS)", "anticonceptivos orales"), ("Tiña pedis", "Dermatofitosis del pie"),
                              ("Cervicalgia", "Cervicalgia"), ("Vaginosis mixta", "Vaginosis"),
                              ("Cuerpo extraño oído izq", "Cuerpo extraño")):
            self.assertIn(nombre, BANK[hb.bank_id(abrev)]["n"], abrev)

    def test_sinonimos_apuntan_a_diagnosticos_que_existen(self):
        from services.hea_data import SINONIMOS
        for k, n in SINONIMOS.items():
            self.assertIn(n, BANK, k)
        for t in ("SDA", "IVU", "OMA", "Lumbociatica", "Hipotiroidismo", "Onicomicosis", "Escabiasis", "Gripe",
                  "Climaterio", "HPB", "ERC", "Artrosis", "Varices", "Pie diabetico", "Dispepsia", "Aftas"):
            self.assertIsNotNone(hb.bank_id(t), t)

    def test_sugerencia_de_lista_no_confunde_abreviaturas(self):
        casos = {"OMA": "Otitis media", "ERC": "Enfermedad renal crónica", "Malaria": "Paludismo",
                 "SDA": "Gastroenteritis", "RC": "Nasofaringitis", "HTA": "Hipertensión esencial",
                 "Escabiasis": "Sarna", "Lumbociatica": "Ciática"}
        for abrev, esperado in casos.items():
            self.assertTrue(hb.sugerir_lista(abrev)[0].startswith(esperado), (abrev, hb.sugerir_lista(abrev)))
        for abrev in ("PF", "EPOC", "XYZ"):
            self.assertEqual(cat.suggest(abrev), [], abrev)   # mejor nada que una opción equivocada

    def test_sin_cifras_inventadas(self):
        for n, b in BANK.items():
            for v in b["v"]:
                self.assertNotRegex(v, r"\d+(?:[.,]\d+)?\s*(?:°C|mg/dl|mmHg)", n)
                self.assertNotRegex(v, r"\by (i|hi)(?![aeiouáéíóú])", n)

    def test_sintoma_principal_sin_lado(self):
        for n, b in BANK.items():
            if b["k"] == "S":
                self.assertNotRegex(b["t"], r"derech|izquierd", n)

    def test_cabecera(self):
        self.assertEqual(hb.cabecera("M", "30"), "Beneficiaria Fem de 30 años de edad, que presenta ")
        self.assertEqual(hb.cabecera("H", "1"), "Beneficiario Masc de 1 año de edad, que presenta ")
        self.assertEqual(hb.cabecera("M", "1", "meses"), "Beneficiaria Fem de 1 mes de edad, que presenta ")
        self.assertEqual(hb.cabecera("", ""), "Beneficiaria/o Fem/Masc, que presenta ")

    def test_cronicos_juntos_sin_repetir(self):
        r = random.Random(3)
        for _ in range(60):
            t, _a = hb.compose("H", "70", ["HTA", "DM2"], rng=r)
            self.assertTrue(t.startswith("Beneficiario Masc de 70 años de edad, que presenta antecedente de "))
            self.assertEqual(len(re.findall(r"diabetes", t.split("Niega")[0], re.I)), 1, t)

    def test_no_nombra_enfermedades_que_no_tiene(self):
        r = random.Random(4)
        for _ in range(100):
            t, _a = hb.compose("M", "50", ["HTA", "Gastritis"], rng=r)
            self.assertNotIn("diabetes", t.lower(), t)

    def test_edad_y_sexo(self):
        r = random.Random(5)
        for _ in range(100):
            t, _a = hb.compose("H", "6", ["Cefalea", "Contractura muscular"], rng=r)
            self.assertNotRegex(t.lower(), r"trabaj|laboral|jornada|computadora|automedic", t)
            t, _a = hb.compose("M", "40", ["Diarrea"], rng=r)
            self.assertNotIn("madre", t.lower(), t)
        t, av = hb.compose("H", "30", ["Candidiasis vulvovaginal"], rng=r)
        self.assertTrue(av)
        t, av = hb.compose("H", "40", ["Dermatosis del pañal"], rng=r)
        self.assertTrue(any("lactantes" in a for a in av))

    def test_negativos_no_contradicen(self):
        r = random.Random(6)
        for _ in range(100):
            t, _a = hb.compose("M", "30", ["Amigdalitis aguda, sin especificación", "Tos"], rng=r)
            neg = " ".join(re.findall(r"Niega [^.]*\.", t)).lower()
            self.assertNotRegex(neg, r"\btos\b", t)

    def test_combinaciones_al_azar(self):
        r = random.Random(0)
        ids = list(BANK)
        for _ in range(3000):
            dx = [BANK[i]["n"] for i in r.sample(ids, r.randint(1, 3))]
            sx = r.choice("MH")
            edad, unidad = r.choice([("1", "meses"), ("2", "años"), ("7", "años"), ("35", "años"), ("72", "años")])
            t, _a = hb.compose(sx, edad, dx, unidad, rng=r)
            self.assertEqual(problemas(t), [], (dx, t))

    def test_mismo_diagnostico_dos_veces(self):
        t, _a = hb.compose("M", "30", ["Gastritis", "Gastritis, sin especificación"], rng=random.Random(1))
        self.assertNotIn("Además", t)



class T09_SignosVitales(unittest.TestCase):
    def test_listas_y_valores_iniciales(self):
        from services import activityinfo as ai
        self.assertEqual((ai.LISTA_SISTOLICA[0], ai.LISTA_SISTOLICA[-1], len(ai.LISTA_SISTOLICA)), ("60", "250", 20))
        self.assertEqual((ai.LISTA_DIASTOLICA[0], ai.LISTA_DIASTOLICA[-1]), ("30", "150"))
        self.assertEqual((len(ai.LISTA_FC), ai.LISTA_FC[0], ai.LISTA_FC[-1]), (161, "40", "200"))
        self.assertEqual((ai.LISTA_FR[0], ai.LISTA_FR[-1]), ("10", "50"))
        self.assertEqual((ai.LISTA_TEMP[0], ai.LISTA_TEMP[-1], ai.LISTA_TEMP[1]), ("35.0", "41.0", "35.1"))
        for _ in range(300):
            m = ai.vitales_defecto("M", "30")
            h = ai.vitales_defecto("H", "30")
            self.assertEqual((m["sistolica"], m["diastolica"], h["diastolica"]), ("120", "70", "80"))
            self.assertTrue(65 <= int(m["fc"]) <= 90 and m["fc"] in ai.LISTA_FC)
            self.assertTrue(12 <= int(m["fr"]) <= 20)
            self.assertTrue(36.0 <= float(m["temperatura"]) <= 37.2 and m["temperatura"] in ai.LISTA_TEMP)
        for edad, unidad in (("10", "años"), ("5", "años"), ("8", "meses"), ("", "años")):
            self.assertEqual(ai.vitales_defecto("H", edad, unidad)["fr"], "", (edad, unidad))
        self.assertTrue(ai.vitales_defecto("H", "11")["fr"])

if __name__ == "__main__":
    unittest.main(verbosity=2)


class T08_BancoNuevo(unittest.TestCase):
    """Banco generado (tools/hea_gen.py): más versiones, sin repetirse, y todas las listas cubiertas."""

    def test_doce_o_mas_versiones_sin_repetirse(self):
        import difflib
        from services.hea_data_gen import BANK_GEN
        self.assertGreaterEqual(len(BANK_GEN), 340)
        for n, b in BANK_GEN.items():
            self.assertGreaterEqual(len(b["v"]), 12, (n, b["n"]))
            self.assertEqual(len(set(b["v"])), len(b["v"]), (n, b["n"]))
            for i, a in enumerate(b["v"]):
                for c in b["v"][i + 1:]:
                    self.assertLess(difflib.SequenceMatcher(None, a, c, autojunk=False).ratio(), .9, (n, b["n"]))

    def test_estructura_de_las_versiones(self):
        from services.hea_data_gen import BANK_GEN
        for n, b in BANK_GEN.items():
            for v in b["v"]:
                self.assertTrue(v.endswith("."), (n, v))
                self.assertFalse(re.search(r"\.\.|,,|\s[,.;]|\by (i|hi)[^aeiouáéíóú\W]", v), (n, v))
                if b["k"] == "C":
                    self.assertTrue(v.startswith("antecedente de "), (n, v))

    def test_toda_la_lista_ssr_tiene_hea_propia(self):
        from services import cie11_ssr as ssr
        for d in ssr.descriptions():
            n = hb.bank_id(d)
            self.assertIsNotNone(n, d)
        self.assertIn("Vaginosis", BANK[hb.bank_id("Vaginosis bacteriana")]["n"])
        self.assertIn("Dismenorrea", BANK[hb.bank_id("Dismenorrea")]["n"])
        self.assertIn("Cervicitis", BANK[hb.bank_id("Cervicitis")]["n"])
        self.assertIn("Mastitis", BANK[hb.bank_id("Mastitis puerperal")]["n"])
        self.assertIn("Prurito vulvar", BANK[hb.bank_id("Prurito vulvar")]["n"])

    def test_hea_con_diagnosticos_de_aps_y_ssr(self):
        r = random.Random(11)
        for _ in range(50):
            t, av = hb.compose("M", "29", ["Cefalea", "Vaginosis bacteriana", "Dismenorrea"], rng=r)
            self.assertNotIn("None", t)
            self.assertEqual(len(re.findall(r"Beneficiaria", t)), 1, t)



class T09_ExamenFisico(unittest.TestCase):
    def test_orden_y_normal(self):
        from services import examen_fisico as e
        t = e.compose([])
        tit = [l.split(":")[0] for l in t.split("\n")]
        self.assertEqual(tit, ["General", "Cabeza", "ORL", "Cuello", "Tórax", "Corazón", "Pulmones", "Abdomen", "Extremidades"])
        self.assertIn("falta de espacio clínico", t)
        self.assertEqual(e.compose([], ssr=True).split("\n")[-1][:14], "Genitourinario")

    def test_vaginitis(self):
        from services import examen_fisico as e
        t = e.compose(["Vaginitis aguda"], ssr=False)
        self.assertIn("Genitourinario", t)
        for w in ("purulento", "amarillento", "fétido", "abundante"):
            self.assertIn(w, t)

    def test_varios_dx(self):
        from services import examen_fisico as e
        t = e.compose(["Amigdalitis aguda, sin especificación", "Cervicalgia"])
        self.assertIn("amígdalas hipertróficas", t)
        self.assertIn("contractura", t)
        self.assertNotIn("Genitourinario", t)

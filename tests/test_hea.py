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
        self.assertEqual(ai.vitales_defecto("H", "", "años")["fr"], "")       # sin edad: FR vacía
        self.assertTrue(ai.vitales_defecto("H", "30")["fr"])

    def test_vitales_pediatricos_por_edad(self):
        from services import activityinfo as ai
        tabla = [  # (edad, unidad, sist, diast, fc, fr) según la tabla de valores normales
            ("0", "días", (65, 85), (45, 55), (110, 160), (30, 60)), ("2", "meses", (65, 85), (45, 55), (110, 160), (30, 60)),
            ("3", "meses", (70, 90), (50, 65), (100, 150), (30, 45)), ("5", "meses", (70, 90), (50, 65), (100, 150), (30, 45)),
            ("6", "meses", (80, 100), (55, 65), (90, 130), (25, 40)), ("11", "meses", (80, 100), (55, 65), (90, 130), (25, 40)),
            ("1", "años", (90, 105), (55, 70), (80, 125), (20, 30)), ("2", "años", (90, 105), (55, 70), (80, 125), (20, 30)),
            ("3", "años", (95, 110), (60, 75), (70, 115), (20, 25)), ("5", "años", (95, 110), (60, 75), (70, 115), (20, 25)),
            ("6", "años", (100, 120), (60, 75), (60, 100), (14, 22)), ("11", "años", (100, 120), (60, 75), (60, 100), (14, 22)),
            ("12", "años", (100, 120), (70, 80), (60, 100), (12, 18)), ("17", "años", (100, 120), (70, 80), (60, 100), (12, 18)),
        ]
        for edad, unidad, sis, dia, fc, fr in tabla:
            vistos = set()
            for _ in range(200):
                v = ai.vitales_defecto("H", edad, unidad)
                vistos.add(v["fc"])
                for k, (lo, hi) in (("sistolica", sis), ("diastolica", dia), ("fc", fc), ("fr", fr)):
                    self.assertTrue(lo <= int(v[k]) <= hi, (edad, unidad, k, v[k]))
            self.assertGreater(len(vistos), 5, (edad, unidad))               # son aleatorios
        adulto = ai.vitales_defecto("M", "18", "años")                         # 18 años: ya es adulto
        self.assertEqual((adulto["sistolica"], adulto["diastolica"]), ("120", "70"))
        self.assertNotEqual(ai.grupo_vitales("H", "4", "años"), ai.grupo_vitales("H", "8", "años"))
        self.assertEqual(ai.grupo_vitales("H", "4", "años"), ai.grupo_vitales("M", "5", "años"))

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

    def test_diagnostico_secundario_con_cuadro_propio(self):
        r = random.Random(4)
        for _ in range(60):
            t, av = hb.compose("M", "26", ["Cefalea", "Vaginosis bacteriana", "Candidiasis vulvovaginal"], rng=r)
            sec = t.split("Además refiere ", 1)[1]
            self.assertGreater(len(sec.split(".")[0].split()), 7, t)       # cuadro descrito, no una etiqueta
            self.assertIn("También refiere", t)
            self.assertNotRegex(t, r"cuadro actual de cuadro|embarazo actual|\.\.")

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
        self.assertNotIn("\n", t)                                   # un solo párrafo, con etiquetas
        etiquetas = ("Apariencia general:", "Cabeza:", "ORL:", "Cuello:", "Tórax:", "Corazón:", "Pulmones:", "Abdomen:",
                     "Genitourinario:", "Extremidades:")
        pos = [t.find(x) for x in etiquetas]
        self.assertNotIn(-1, pos)
        self.assertEqual(pos, sorted(pos))                          # genitourinario justo después del abdomen
        self.assertIn("falta de espacio clínico", t)
        self.assertIn("No se realiza inspección genital debido a la ausencia de un espacio físico privado y adecuado, así como "
                      "de camilla e instrumental necesario", t)
        self.assertNotIn("espécul", t)
        self.assertEqual(e.compose([], ssr=True), t)

    def test_vaginitis(self):
        from services import examen_fisico as e
        t = e.compose(["Vaginitis aguda"], ssr=False)
        self.assertIn("No se realiza inspección genital", t)         # no se explora: no se inventan hallazgos genitales
        self.assertNotIn("purulento", t)
        emb = e.compose(["Estado de embarazo"])                       # hallazgos que no requieren explorar sí se conservan
        self.assertIn("altura uterina", emb)
        self.assertIn("No se realiza inspección genital", emb)
        self.assertNotIn("espécul", emb)

    def test_varios_dx(self):
        from services import examen_fisico as e
        t = e.compose(["Amigdalitis aguda, sin especificación", "Cervicalgia"])
        self.assertIn("amígdalas hipertróficas", t)
        self.assertIn("contractura", t)
        self.assertIn("puño percusión", e.compose(["Infección urinaria, sitio no especificado"]))

    def test_dx_como_en_el_ata(self):
        from services import examen_fisico as e
        t = e.compose(["HTA", "Dermatitis"])
        self.assertIn("Piel y faneras: Lesiones", t)
        self.assertNotIn("uñas y cabello de implantación", t)

    def test_variantes(self):
        import random
        from services import examen_fisico as e
        textos = {e.compose(["Faringitis aguda"], ssr=True, rng=random.Random(i)) for i in range(30)}
        self.assertGreater(len(textos), 10)
        for t in textos:
            self.assertIn("No se realiza inspección genital", t)
            self.assertRegex(t, r"Genitourinario: .*Extremidades: .*Piel y faneras: ")
            self.assertNotRegex(t, r"Apariencia general: [^.]*\. Piel")

    def test_cobertura_y_correcciones(self):
        from services import cie11_catalog as cat, cie11_ssr as ssr
        from services import examen_fisico as e
        sin = [d for m in (cat, ssr) for d in m.descriptions() if not e._hallazgos([d])]
        self.assertLessEqual(len(sin), 2, sin)                     # solo «otros síntomas… no clasificados»
        self.assertIn("piel", e._hallazgos(["Afecciones alérgicas o de hipersensibilidad, sin especificación"]))
        self.assertIn("oidos", e._hallazgos(["Otitis media, sin especificación"]))
        self.assertIn("piel", e._hallazgos(["Uña encarnada"]))
        self.assertEqual(list(e._hallazgos(["Hemorragia retiniana"])), ["ojos"])
        t = e.compose(["Hipertensión esencial, sin especificación"])
        self.assertEqual(t.lower().count("ingurgitación yugular"), 1)


class T10_PlanBanco(unittest.TestCase):
    def test_cobertura_y_forma(self):
        import random
        import re
        from services import cie11_catalog as cat, cie11_ssr as ssr
        from services import plan_banco as pb
        for m in (cat, ssr):
            for d in m.descriptions():
                self.assertTrue(pb.tiene_plan(d), d)
                reg = pb.PLAN[d]
                self.assertTrue(4 <= len(reg["m"]) <= 13 and 4 <= len(reg["a"]) <= 9, d)
                self.assertTrue(all(re.match(r"[a-záéíóúñü]+(ar|er|ir|se|le|la|lo)\b|(en|si|al|ante|durante|después|con|cuando) ", x) for x in reg["m"]), d)
                t = pb.compose([d], rng=random.Random(1))
                self.assertTrue(t.endswith(".") and "alarma" in t and t[0].isupper(), d)
                self.assertNotRegex(t, r"Indicaciones generales|Debe consultar|Se sugiere", d)
                self.assertNotRegex(t, r"\b\d+\s?mg\b", d)                  # nunca dosis de medicamentos

    def test_varias_versiones_y_varios_dx(self):
        import random
        from services import plan_banco as pb
        dx = ["Hipertensión esencial, sin especificación", "Cervicitis"]
        textos = {pb.compose(dx, rng=random.Random(i)) for i in range(25)}
        self.assertGreater(len(textos), 15)
        self.assertEqual(pb.compose(dx), pb.compose(dx))                   # sin rng: estable
        t = pb.compose(dx, rng=random.Random(3)).lower()
        self.assertRegex(t, "alarma")
        self.assertEqual(pb.compose([]), "")


class T11_PlanificacionFamiliar(unittest.TestCase):
    """La HEA de PF habla del método que dice el ATA (antes toda salía con la inyección trimestral)."""
    METODOS = {"oral": r"inyecci|inyectable|depo|medroxi|trimestral|implante|dispositivo|DIU\b|condón",
               "depo": r"pastilla|oral|implante|dispositivo|DIU\b|condón|mensual",
               "implante": r"pastilla|oral|inyecci|inyectable|depo|medroxi|trimestral|dispositivo|DIU\b",
               "diu": r"pastilla|oral|inyecci|inyectable|depo|medroxi|implante|trimestral",
               "condon": r"pastilla|oral|inyecci|inyectable|depo|medroxi|implante|dispositivo|DIU\b",
               "generico": r"pastilla|oral|inyecci|inyectable|depo|medroxi|trimestral|implante|dispositivo|DIU\b|condón"}

    def test_el_metodo_se_detecta_del_texto_del_ata(self):
        from services import hea_pf
        casos = {"PF (ACOs)": "oral", "PF (ACOS) 3 meses": "oral", "PF aco": "oral", "PF Depo": "depo",
                 "PF (Depo) 3 meses": "depo", "PF inyectable": "inyectable", "PF mensual": "mensual",
                 "PF implante": "implante", "PF (Jadelle)": "implante", "PF DIU": "diu", "PF condón": "condon",
                 "PF": None, "Contacto con los servicios de salud para atención relativa a la anticoncepción": None}
        for t, m in casos.items():
            self.assertEqual(hea_pf.metodo(t), m, t)
        self.assertEqual(hb.bank_id("PF (ACOS) 3 meses"), 326)        # antes: sin HEA por los paréntesis
        self.assertEqual(hb.bank_id("PF (Depo) 3 meses"), 152)
        self.assertEqual(hb.bank_id("PF implante"), 152)

    def test_cada_metodo_habla_solo_de_su_metodo(self):
        for texto, m in (("PF (ACOs)", "oral"), ("PF (ACOS) 3 meses", "oral"), ("PF (Depo)", "depo"),
                         ("PF implante", "implante"), ("PF condón", "condon"), ("PF", "generico"),
                         ("Contacto con los servicios de salud para atención relativa a la anticoncepción", "generico")):
            for i in range(120):
                t = hb.compose("M", "30", [texto], "años", random.Random(i))[0]
                self.assertEqual(problemas(t), [], (texto, t))
                self.assertNotRegex(t, self.METODOS[m], (texto, t))
        for i in range(120):                                           # y las pastillas sí salen con ACOs
            t = hb.compose("M", "30", ["PF (ACOs)"], "años", random.Random(i))[0]
            self.assertRegex(t.lower(), r"pastilla|anticonceptivos orales", t)
            t = hb.compose("M", "30", ["PF (Depo)"], "años", random.Random(i))[0]
            self.assertRegex(t.lower(), r"inyecci|inyectable", t)

    def test_muchas_versiones_por_metodo(self):
        from services import hea_pf
        for m, v in hea_pf.VERSIONES.items():
            self.assertGreaterEqual(len(set(v)), 16, m)
            for x in v:
                self.assertRegex(x, r"^(acude|utiliza|solicita|refiere|es portadora)\b", (m, x))
                self.assertNotRegex(x, r"\by (i|hi)(?![aeiouáéíóú])|___|  ", (m, x))
        t = {hb.compose("M", "30", ["PF (ACOs)"], "años", random.Random(i))[0] for i in range(80)}
        self.assertGreater(len(t), 25)

    def test_pf_junto_a_otro_diagnostico_conserva_el_metodo(self):
        t = hb.compose("M", "44", ["Cefalea", "PF (ACOs)"], "años", random.Random(5))[0]
        self.assertIn("anticonceptivos orales", t)
        self.assertNotIn("inyectable", t)
        t = hb.compose("M", "44", ["HTA", "PF (Depo)"], "años", random.Random(5))[0]
        self.assertIn("inyectable trimestral", t)

    def test_fuente_ssr_usa_el_texto_del_ata_solo_si_es_la_sugerencia(self):
        self.assertEqual(hb.fuente_hea_ssr("PF (ACOs)", "Contacto con los servicios de salud para atención relativa a la anticoncepción", True), "PF (ACOs)")
        self.assertEqual(hb.fuente_hea_ssr("PF (ACOs)", "Contacto con los servicios de salud para anticoncepción poscoital", False),
                         "Contacto con los servicios de salud para anticoncepción poscoital")
        self.assertEqual(hb.fuente_hea_ssr("XYZ", "Vaginosis bacteriana", True), "Vaginosis bacteriana")

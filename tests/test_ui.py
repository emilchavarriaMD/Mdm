"""Pruebas de la interfaz Tkinter (necesitan pantalla; en Linux: xvfb-run -a python -m unittest tests.test_ui).

Los cuadros de diálogo se simulan: se registran y se devuelve la respuesta predeterminada
o la que la prueba indique.
"""
import os
import shutil
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
_TMP = tempfile.mkdtemp(prefix="brigadas_ui_")
os.environ["BRIGADAS_DATA_DIR"] = _TMP

try:
    import tkinter as tk
    _t = tk.Tk()
    _t.destroy()
    HAS_DISPLAY = True
except Exception:  # noqa: BLE001
    HAS_DISPLAY = False

if HAS_DISPLAY:
    import config
    from database import Database
    from ui import dialogs, widgets
    from ui.app import App

TODAY = date.today().strftime("%d/%m/%Y")


@unittest.skipUnless(HAS_DISPLAY, "sin pantalla disponible")
class UITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = Database(config.db_path())
        cls.app = App(cls.db)
        cls.root = cls.app.root
        cls.root.deiconify()
        cls.log = []
        cls.answers = []

        def choose(parent, title, message, buttons, default=None, cancel=None, details=None):
            cls.log.append((title, message, details))
            return cls.answers.pop(0) if cls.answers else default

        dialogs.choose = choose
        cls.errors = []
        dialogs.show_errors = lambda parent, errors, title="": cls.errors.append(list(errors))
        dialogs.ask_save_path = lambda *a, **k: None
        cls.root.report_callback_exception = lambda et, e, tb: (_ for _ in ()).throw(e)

    @classmethod
    def tearDownClass(cls):
        try:
            cls.root.destroy()
        except tk.TclError:
            pass
        shutil.rmtree(_TMP, ignore_errors=True)

    def setUp(self):
        self.answers.clear()
        self.errors.clear()
        self.log.clear()

    def upd(self):
        self.root.update_idletasks()
        self.root.update()

    # ------------------------------------------------------------------
    def test_00_todas_las_paginas_abren(self):
        for name in ("ata", "pacientes", "backup", "settings"):
            self.assertTrue(self.app.show(name))
            self.upd()

    def test_01_formato_de_fecha(self):
        de = widgets.DateEntry(self.root)
        de.var.set("12032026")
        de._on_key(SimpleNamespace(keysym="6", char="6"))
        self.assertEqual(de.get_value(), "12/03/2026")
        de.set_value("2026-10-05")
        self.assertEqual(de.get_value(), "05/10/2026")

    def test_02b_botones_de_la_tabla(self):
        from ui import dialogs
        app = self.app
        app.show("ata")
        pg = app.pages["ata"]
        self.upd()
        orig_conf, orig_info = dialogs.confirm, dialogs.info
        dialogs.confirm = lambda *a, **k: True
        dialogs.info = lambda *a, **k: None
        try:
            pg.new(force=True)
            self.assertEqual(len(pg.cells), 20)
            pg.cells[0]["nombre"].set("Ana")
            pg.cells[1]["nombre"].set("Luis")
            pg.cells[3]["nombre"].set("Marta")
            pg.add_line()
            self.assertEqual(len(pg.cells), 21)
            pg._foco = 1                                   # cursor en la línea 2
            pg.duplicate_line()
            self.assertEqual([r["nombre"].get() for r in pg.cells[:3]], ["Ana", "Luis", "Luis"])
            self.assertEqual(pg.cells[2]["numero"].get(), "3")
            pg._foco = 2
            pg.delete_line()
            self.assertEqual([r["nombre"].get() for r in pg.cells[:3]], ["Ana", "Luis", ""])
            pg.remove_empty()
            self.assertEqual([r["nombre"].get() for r in pg.cells], ["Ana", "Luis", "Marta"])
            self.assertEqual([r["numero"].get() for r in pg.cells], ["1", "2", "3"])
            pg._foco = None
            pg.delete_line()                               # sin línea elegida: no borra nada
            self.assertEqual(len(pg.cells), 3)
            pg.clear_lines()
            self.assertEqual(len(pg.cells), 20)
            self.assertTrue(all(not r["nombre"].get() for r in pg.cells))
        finally:
            dialogs.confirm, dialogs.info = orig_conf, orig_info

    def test_02_hoja_ata_y_pacientes(self):
        from PIL import Image
        from services import ata as A
        app, db = self.app, self.db
        app.show("ata")
        pg = app.pages["ata"]
        self.upd()
        pg.h["establecimiento"].set("Del Carmen")
        c = pg.cells
        for k, v in {"nombre": "Ana Pérez", "sexo": "m", "edad_anios": "43", "dep": "Cortés",
                     "mun": "Choloma", "loc": "Col. Rafael", "dx1": "Gastritis"}.items():
            c[0][k].set(v)
        c[1]["nombre"].set("Luis Gómez")
        c[1]["sexo"].set("h")
        for k in ("dep", "mun", "loc"):
            c[1][k].set('"')
        c[2]["nombre"].set("Sin sexo")
        c[2]["sexo"].set("X")
        self.assertFalse(pg.save())
        self.assertTrue(self.errors)
        c[2]["sexo"].set("")
        c[2]["fecha_nacimiento"].set("31/02/2000")
        self.assertFalse(pg.save())
        c[2]["fecha_nacimiento"].set("")
        self.assertTrue(pg.save())
        sheet, rows = A.get_sheet(db, pg.sheet_id)
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[1]["loc"], "Col. Rafael")
        self.assertEqual(rows[0]["sexo"], "M")
        self.assertEqual(rows[2]["dx1"], "")
        self.assertEqual(rows[0]["ai_estado"], "Pendiente")
        A.set_llenado(db, rows[2]["id"])                              # formulario llenado, ficha aún sin crear
        self.assertEqual(A.get_record(db, rows[2]["id"])["ai_estado"], "Llenado")
        self.assertEqual(len(A.list_records(db, "", "Llenado")), 1)
        A.set_registered(db, rows[2]["id"], True)
        A.set_llenado(db, rows[2]["id"])                              # no pisa un «Registrado»
        self.assertEqual(A.get_record(db, rows[2]["id"])["ai_estado"], "Registrado")
        A.set_registered(db, rows[2]["id"], False)

        # lista de pacientes y estado de ActivityInfo
        app.show("pacientes")
        pp = app.pages["pacientes"]
        self.upd()
        self.assertEqual(len(pp.tree.get_children()), 3)
        pp.q.set_value("luis")
        pp.load()
        self.assertEqual(len(pp.tree.get_children()), 1)
        rid = int(pp.tree.get_children()[0])
        from services import activityinfo
        import ui.page_pacientes as ppmod
        activityinfo.save_dx_map(db, "gastritis", "Gastritis", "DA42")
        seen = {}

        class FakeDialog:
            def __init__(self, parent, defaults, db=None):
                seen["defaults"] = defaults

            def run(self):
                d = dict(seen["defaults"])
                d["estado_civil"] = "Soltero/a"
                return d

        ppmod.ActivityInfoDialog = FakeDialog
        self.addCleanup(setattr, activityinfo, "fill_form", activityinfo.fill_form)     # que el simulacro no se quede puesto
        activityinfo.fill_form = lambda data, **k: (seen.update(sent=data) or {"ficha": ["Perfil: falta"], "aps": []})
        pp.tree.selection_set(str(rid))
        self.answers[:] = ["ok", "yes"]  # aviso final y «marcar como registrado»
        pp.add_record()
        for _ in range(80):
            self.upd()
            if pp._result is None and self.log and len(self.log) >= 2:
                break
            import time as _t
            _t.sleep(0.05)
        self.assertEqual(seen["defaults"]["nombres"], "Luis")
        self.assertEqual(seen["defaults"]["genero"], "Hombre CIS")
        self.assertEqual(seen["defaults"]["tiene_fecha_nac"], "No")
        self.assertEqual(seen["defaults"]["perfil"], "Persona en riesgo de desplazamiento")
        self.assertEqual(seen["defaults"]["idioma"], "Español")
        self.assertEqual((seen["defaults"]["donante"], seen["defaults"]["proyecto"], seen["defaults"]["perfin"]),
                         ("ECHO", "ECHO - COMPASS", "F09010020"))
        self.assertEqual(seen["defaults"]["pueblo"], "Ladino / Mestizo")      # valor por defecto
        self.assertTrue(seen["defaults"]["hea"].startswith("Beneficiario Masc"))
        self.assertEqual(seen["sent"]["estado_civil"], "Soltero/a")
        self.assertEqual(seen["defaults"]["estado_civil"], "Unión Libre")      # lo que el ATA no trae: valor por defecto
        self.assertEqual(A.get_record(db, rid)["ai_estado"], "Registrado")
        # guardar de nuevo la hoja conserva el estado registrado
        app.show("ata")
        pg._open(sheet["id"])
        self.assertTrue(pg.save())
        self.assertEqual(A.get_record(db, db.scalar("SELECT id FROM ata_rows WHERE nombre='Luis Gómez'"))["ai_estado"],
                         "Registrado")
        pp.q.set_value("")
        pp.estado.set_value("Pendiente")
        app.show("pacientes")
        pp.load()
        self.assertEqual(len(pp.tree.get_children()), 2)
        # selección y borrado
        pp.estado.set_value("Todos")
        pp.load()
        pp.toggle_all()
        self.assertEqual(len(pp._checked), 3)
        pp.toggle_all()
        self.assertEqual(len(pp._checked), 0)
        first = int(pp.tree.get_children()[0])
        pp.tree.selection_set(str(first))
        pp.toggle_current()
        self.assertEqual(pp._checked, {first})
        self.answers[:] = ["yes"]
        pp.delete_checked()
        self.assertEqual(len(pp.tree.get_children()), 2)
        self.assertEqual(self.db.scalar("SELECT COUNT(*) FROM ata_rows WHERE borrado_en IS NULL"), 2)
        self.assertEqual(self.db.scalar("SELECT COUNT(*) FROM ata_rows WHERE borrado_en IS NOT NULL"), 1)   # en la papelera
        # filtros de sexo y edad, y alerta de la fila seleccionada
        pp.sexo.set_value("Hombre")
        pp.load()
        self.assertTrue(all(pp._rows[int(i)]["sexo"] == "H" for i in pp.tree.get_children()))
        pp.sexo.set_value("Todos")
        pp.grupo.set_value("60 años o más")
        pp.load()
        self.assertEqual(len(pp.tree.get_children()), 0)
        pp.grupo.set_value("Todas las edades")
        pp.load()
        self.assertEqual(len(pp.tree.get_children()), 2)
        import ui.page_pacientes as ppmod2

        class NoDialog:
            def __init__(self, *a, **k):
                pass

            def run(self):
                return None
        ppmod2.ActivityInfoDialog = NoDialog
        pp.tree.selection_set(pp.tree.get_children()[0])
        pp.siguiente_pendiente()                      # abre el siguiente pendiente (aquí se cancela el diálogo)
        self.assertEqual(pp.progreso["maximum"], 100)

    def test_03_importar_excel_y_exportar(self):
        from services import ata as A
        app, db = self.app, self.db
        app.show("ata")
        pg = app.pages["ata"]
        pg.new(force=True)
        header = {"establecimiento": "Del Carmen", "fecha": "2026-10-15", "municipio": "Choloma"}
        rows = [{**{k: "" for k in A.KEYS}, "numero": "1", "nombre": "Paciente Uno", "sexo": "H",
                 "edad_meses": "7", "dx1": "RC", "dep": "Cortés", "fecha_nacimiento": "2020-01-05"}]
        out = Path(_TMP) / "importar.xlsx"
        A.export_excel(out, header, rows)
        import ui.page_ata as pa
        pa.dialogs.ask_open_path = lambda *a, **k: str(out)
        pg.load_excel()
        self.assertEqual(pg.cells[0]["nombre"].get(), "Paciente Uno")
        self.assertEqual(pg.cells[0]["fecha_nacimiento"].get(), "05/01/2020")
        self.assertEqual(pg.h["establecimiento"].get(), "Del Carmen")
        self.assertTrue(pg.is_dirty())  # aún sin confirmar
        self.assertTrue(pg.save())
        self.assertEqual(A.get_sheet(db, pg.sheet_id)[1][0]["edad_meses"], "7")

    def test_04_activityinfo_nunca_guarda(self):
        from services import activityinfo as ai
        src = (ROOT / "services" / "ai_fill.js").read_text(encoding="utf-8")
        self.assertIn("guardar|save|est[aá] hecho|cancelar", src)  # lista de botones bloqueados
        self.assertNotIn(".submit(", src)
        d = ai.build_defaults(self.db, {"nombre": "Ana Pérez López", "sexo": "M", "fecha": "2026-10-15",
                                        "edad_meses": "7", "dx1": "HTA", "dx2": "", "dx3": ""})
        self.assertEqual(d["genero"], "Mujer CIS")
        self.assertEqual(d["edad"], "0")
        self.assertEqual(d["lugar"], "San Pedro Sula")
        self.assertEqual(d["punto_especifico"], "")
        d2 = ai.build_defaults(self.db, {"nombre": "Ana", "sexo": "M", "edad_anios": "30", "fecha": "2026-10-15",
                                         "loc": " Brisas 1 ", "dx1": "HTA"})
        self.assertEqual(d2["punto_especifico"], "Brisas 1")
        self.assertEqual(d["dx"][0]["descripcion"], "")  # sin equivalencia: no se inventa
        p = ai.payload(d)
        self.assertEqual(p["n_dx"], 1)
        self.assertEqual(p["dx"][0]["abrev"], "HTA")

    def test_04b_ventana_con_varias_consultas(self):
        from services import activityinfo as ai
        from ui.dialog_activityinfo import ActivityInfoDialog
        d = ai.build_defaults(self.db, {"nombre": "Ana Pérez López", "sexo": "M", "fecha": "2026-10-15",
                                        "edad_anios": "30"})
        self.assertEqual(d["consultas"], [ai.CONSULTA_APS])
        dlg = ActivityInfoDialog(self.root, d)
        dlg.w["consultas"].set_value([ai.CONSULTA_APS, "Nutrición"])
        for k, v in {"estado_civil": "Soltero/a", "escolaridad": "Primaria", "ocupacion": "Estudiante",
                     "discapacidad": "No", "derivado": "No", "tipo_consulta": "Primera"}.items():
            dlg.w[k].set_value(v)
        dlg._ok()
        self.assertEqual(dlg.result["consultas"], [ai.CONSULTA_APS, "Nutrición"])
        self.assertEqual(dlg.result["tiene_fecha_nac"], "No")
        self.assertEqual(dlg.result["edad"], "30")
        self.assertEqual(ai.payload(dlg.result)["consultas"], [ai.CONSULTA_APS, "Nutrición"])

    def test_04c_diagnosticos_lista_activityinfo(self):
        from services import activityinfo as ai
        from services import cie11_catalog as cat
        from ui.dialog_activityinfo import ActivityInfoDialog
        self.assertEqual(len(cat.CATALOG), 260)
        self.assertEqual(cat.suggest("HTA")[0][1], "BA00.Z")
        self.assertEqual(cat.suggest("zzzz"), [])
        d = ai.build_defaults(self.db, {"nombre": "Ana", "sexo": "M", "edad_anios": "30", "fecha": "2026-10-15",
                                        "dx1": "Gastritis", "dx2": "RC", "dx3": "HTA"})
        dlg = ActivityInfoDialog(self.root, d, db=self.db)
        self.assertEqual(len(dlg.dx_rows), 3)
        self.assertIn("DA42.Z", dlg.dx_rows[0][1].get_value())      # sugerido de la lista
        dlg.dx_rows[1][1].set_value("")                              # sin equivalente: no se llena
        dlg.w["consultas"].set_value([ai.CONSULTA_APS])
        for k, v in {"estado_civil": "Soltero/a", "escolaridad": "Primaria", "ocupacion": "Estudiante",
                     "discapacidad": "No", "derivado": "No", "tipo_consulta": "Primera"}.items():
            dlg.w[k].set_value(v)
        dlg._ok()
        self.assertEqual([x["cie11"] for x in dlg.result["dx"]], ["DA42.Z", "BA00.Z"])
        ai.remember_dx(self.db, dlg.result)
        self.assertEqual(ai.dx_map(self.db)["hta"]["cie11"], "BA00.Z")
        self.assertEqual(ai.payload(dlg.result)["n_dx"], 2)

    def test_04d_hea_varios_diagnosticos(self):
        import random
        from services import hea_banco as hb
        r = random.Random(1)
        t, av = hb.compose("H", "58", ["Hipertensión esencial, sin especificación",
                                       "Diabetes mellitus, tipo no especificado"], rng=r)
        self.assertTrue(t.startswith("Beneficiario Masc de 58 años de edad, que presenta antecedente de "))
        self.assertIn("diabetes mellitus", t)
        self.assertIn("hipertensión arterial", t)
        t, av = hb.compose("M", "30", ["Rinitis alérgica, sin especificación", "Tos",
                                       "Trastornos de cefalea, sin especificación"], rng=r)
        self.assertIn("antecedente de rinitis alérgica y cuadro actual de", t)
        self.assertIn("Además refiere", t)
        t, av = hb.compose("H", "30", ["Candidiasis vulvovaginal"], rng=r)
        self.assertTrue(av)
        for d, _c in __import__("services.cie11_catalog", fromlist=["x"]).CATALOG:
            self.assertIsNotNone(hb.bank_id(d), d)

    def test_04e_hea_se_actualiza_y_respeta_lo_editado(self):
        from ui.dialog_activityinfo import ActivityInfoDialog
        d = {"dx": [{"abrev": "RC", "descripcion": "", "cie11": ""}, {"abrev": "Cervicalgia", "descripcion": "",
                                                                     "cie11": ""}],
             "consultas": [], "hea_persona": {"sexo": "", "edad": "5", "unidad": "años"}, "hea": "", "edad": "5"}
        dlg = ActivityInfoDialog(self.root, d)
        dlg._regen_hea(False)
        self.assertIn("Beneficiaria/o Fem/Masc de 5 años", dlg.hea.get("1.0", "end"))
        self.assertEqual([t.cget("text") for t in dlg.dx_tags],
                         ["HEA usa: Nasofaringitis aguda", "HEA usa: Cervicalgia"])
        dlg.w["genero"].set_value("Hombre CIS")
        dlg._regen_hea(True)
        self.assertIn("Beneficiario Masc de 5 años", dlg.hea.get("1.0", "end"))
        dlg.hea.insert("end", " EDITADO")
        dlg.w["edad"].set_value("7")
        dlg._regen_hea(True)
        self.assertIn("EDITADO", dlg.hea.get("1.0", "end"))      # lo escrito a mano no se pisa
        dlg._regen_hea(False)                                     # «Otra versión» sí lo cambia
        self.assertIn("Beneficiario Masc de 7 años", dlg.hea.get("1.0", "end"))
        self.assertEqual(dlg.examen.get("1.0", "end").strip(), "")          # sin valor inicial en este caso
        # derivación: vacía por defecto y sin los demás campos hasta elegir Sí
        self.assertEqual(dlg.w["va_derivado"].get_value(), "")
        dlg.update()
        self.assertFalse(dlg.der_extra.winfo_ismapped())
        dlg.w["va_derivado"].set_value("Sí")
        dlg._mostrar_derivacion()
        dlg.update()
        self.assertTrue(dlg.der_extra.winfo_ismapped())
        dlg.destroy()
        dlg = ActivityInfoDialog(self.root, dict(d, examen_fisico="Cefalo-caudal"))
        self.assertEqual(dlg.examen.get("1.0", "end").strip(), "Cefalo-caudal")
        dlg.destroy()

    def test_04i_panel_paciente(self):
        from ui.dialog_activityinfo import ActivityInfoDialog
        d = {"dx": [{"abrev": "RC", "descripcion": "", "cie11": ""}, {"abrev": "Cervicalgia", "descripcion": "", "cie11": ""}],
             "consultas": [], "hea_persona": {"sexo": "H", "edad": "4", "unidad": "años"}, "hea": "", "edad": "4",
             "nombres": "Luis", "apellidos": "Pérez López", "genero": "Hombre CIS"}
        dlg = ActivityInfoDialog(self.root, d)
        dlg.update()
        self.assertEqual(dlg._p_nombre.winfo_manager(), "pack")
        self.assertIn("Luis Pérez López", dlg._p_nombre.cget("text"))
        self.assertIn("4 años", dlg._p_edad.cget("text"))
        self.assertIn("Hombre", dlg._p_edad.cget("text"))
        self.assertIn("Cervicalgia", dlg._p_dx.cget("text"))
        dlg.w["edad"].set_value("7")
        dlg._refrescar_panel()
        self.assertIn("7 años", dlg._p_edad.cget("text"))
        dlg.destroy()

    def test_04j_valores_por_defecto_de_ficha_y_aps(self):
        from services import activityinfo as ai
        from ui.dialog_activityinfo import ActivityInfoDialog
        escol, ocup = set(), set()
        for _ in range(60):
            d = ai.build_defaults(self.db, {"nombre": "Ana Pérez López", "sexo": "M", "fecha": "2026-10-15", "edad_anios": "30",
                                            "dx1": "Cefalea"})
            escol.add(d["escolaridad"]); ocup.add(d["ocupacion"])
            self.assertEqual((d["lgtbiq"], d["pueblo"], d["estado_civil"], d["discapacidad"], d["derivado"]),
                             ("No", "Ladino / Mestizo", "Unión Libre", "No", "No"))
            self.assertEqual((d["tipo_consulta"], d["va_derivado"], d["ssr_va_derivado"], d["ssr_tipo"]),
                             ("Primera", "No", "No", "Primera"))
        self.assertEqual(escol, {"Primaria", "Secundaria/Bachillerato"})                       # al azar entre las dos
        self.assertEqual(ocup, {"Trabajo doméstico NO remunerado", "Otro"})
        dlg = ActivityInfoDialog(self.root, d)
        self.upd()
        for k, v in {"lgtbiq": "No", "pueblo": "Ladino / Mestizo", "estado_civil": "Unión Libre", "discapacidad": "No",
                     "derivado": "No", "tipo_consulta": "Primera", "va_derivado": "No"}.items():
            self.assertEqual(dlg.w[k].get_value(), v, k)
        self.assertIn(dlg.w["escolaridad"].get_value(), ("Primaria", "Secundaria/Bachillerato"))
        self.assertIn(dlg.w["ocupacion"].get_value(), ("Trabajo doméstico NO remunerado", "Otro"))
        dlg.destroy()

    def test_04k_signos_vitales_con_hta_y_temperatura_sin_decimales(self):
        from services import activityinfo as ai
        from services import cie11_catalog as cat
        from ui.dialog_activityinfo import ActivityInfoDialog
        cat_label = cat.label
        sis, dia, temp = set(), set(), set()
        for _ in range(80):
            d = ai.build_defaults(self.db, {"nombre": "Ana Pérez López", "sexo": "M", "fecha": "2026-10-15", "edad_anios": "55",
                                            "dx1": "HTA"})
            sis.add(d["sistolica"]); dia.add(d["diastolica"]); temp.add(d["temperatura"])
        self.assertEqual((sis, dia, temp), ({"140", "130"}, {"90", "80"}, {"36", "37"}))
        d = ai.build_defaults(self.db, {"nombre": "Luis Pérez", "sexo": "H", "fecha": "2026-10-15", "edad_anios": "55", "dx1": "Cefalea"})
        self.assertEqual((d["sistolica"], d["diastolica"]), ("120", "80"))                    # sin HTA: valores habituales
        for edad, un in (("4", "años"), ("3", "meses"), ("20", "días")):                      # la temperatura sin decimales en todas las edades
            for _ in range(30):
                self.assertIn(ai.vitales_defecto("H", edad, un)["temperatura"], ("36", "37"))
        # al agregar o quitar HTA en la ventana, los signos vitales se proponen de nuevo (si no se tocaron)
        d = ai.build_defaults(self.db, {"nombre": "Ana Pérez López", "sexo": "M", "fecha": "2026-10-15", "edad_anios": "55", "dx1": "Cefalea"})
        dlg = ActivityInfoDialog(self.root, d)
        self.upd()
        self.assertEqual((dlg.w["sistolica"].get_value(), dlg.w["diastolica"].get_value()), ("120", "70"))
        dlg.dx_rows[0][1].set_value(cat_label("Hipertensión esencial, sin especificación"))
        dlg._regen_hea(True)
        self.assertIn(dlg.w["sistolica"].get_value(), ("140", "130"))
        self.assertIn(dlg.w["diastolica"].get_value(), ("90", "80"))
        dlg.w["diastolica"].set_value("85")                                                   # lo escrito a mano no se pisa
        dlg.dx_rows[0][1].set_value(cat_label("Cefalea"))
        dlg._regen_hea(True)
        self.assertEqual((dlg.w["sistolica"].get_value(), dlg.w["diastolica"].get_value()), ("120", "85"))
        self.assertIn("36", list(dlg.w["temperatura"]["values"]))                            # la lista trae grados enteros
        dlg.destroy()

    def test_04m_tipo_de_discapacidad_solo_si_es_si(self):
        from services import activityinfo as ai
        from ui.dialog_activityinfo import ActivityInfoDialog
        dlg = ActivityInfoDialog(self.root, ai.build_defaults(self.db, {
            "nombre": "Ana Pérez López", "sexo": "M", "fecha": "2026-10-15", "edad_anios": "30", "dx1": "Cefalea"}), db=self.db)
        self.assertEqual(dlg.w["discapacidad"].get_value(), "No")
        self.assertFalse(dlg._disc_tipo.winfo_ismapped() and dlg._disc_tipo.winfo_manager())
        dlg.w["discapacidad"].set_value("Sí"); dlg._mostrar_disc(); dlg.update_idletasks()
        self.assertTrue(dlg._disc_tipo.winfo_manager())
        dlg.w["discapacidad_tipo"].set_value(["Mental", "Sensorial"])
        self.assertEqual(dlg.w["discapacidad_tipo"].get_value(), ["Mental", "Sensorial"])
        dlg.w["discapacidad"].set_value("No"); dlg._mostrar_disc()
        self.assertEqual(dlg.w["discapacidad_tipo"].get_value(), [])
        self.assertEqual(ai.payload({"discapacidad": "No", "discapacidad_tipo": ["Mental"], "dx": []})["discapacidad_tipo"], [])
        dlg.destroy()

    def test_04q_lugar_de_atencion_segun_el_ata(self):
        from services import activityinfo as ai
        base = {"nombre": "Ana", "sexo": "M", "fecha": "2026-10-15", "edad_anios": "30", "dx1": "HTA"}
        self.assertEqual(ai.build_defaults(self.db, dict(base, mun="Choloma"))["lugar"], "Choloma")
        self.assertEqual(ai.build_defaults(self.db, dict(base, mun="CHOLOMA, Cortés"))["lugar"], "Choloma")
        self.assertEqual(ai.build_defaults(self.db, dict(base, mun="San Pedro Sula"))["lugar"], "San Pedro Sula")
        self.assertEqual(ai.build_defaults(self.db, dict(base, mun="", mun_hoja="Choloma"))["lugar"], "Choloma")
        self.assertEqual(ai.build_defaults(self.db, dict(base, mun="Villanueva"))["lugar"], "San Pedro Sula")   # sin dato: Configuración
        self.assertEqual(ai.build_defaults(self.db, dict(base, mun="Choloma", mun_hoja="San Pedro Sula"))["lugar"], "San Pedro Sula")   # manda la hoja
        self.assertEqual(ai.build_defaults(self.db, dict(base, mun="Choloma", mun_hoja=""))["lugar"], "Choloma")

    def test_04p_victima_sexual_por_defecto_no(self):
        from services import activityinfo as ai
        d = ai.build_defaults(self.db, {"nombre": "Ana", "sexo": "M", "fecha": "2026-10-15", "edad_anios": "30", "dx1": "Vaginosis"})
        self.assertEqual(d["ssr_victima_sexual"], "No")

    def test_04o_derivacion_desde_y_vineta_de_ssr(self):
        from services import activityinfo as ai
        from ui.dialog_activityinfo import ActivityInfoDialog
        dlg = ActivityInfoDialog(self.root, ai.build_defaults(self.db, {
            "nombre": "Ana", "sexo": "M", "fecha": "2026-10-15", "edad_anios": "30", "dx1": "Vaginosis"}), db=self.db)
        self.assertEqual(dlg.w["derivado"].get_value(), "No")
        dlg.update_idletasks()
        self.assertFalse(dlg.w["derivado_procedencia"].winfo_ismapped())
        dlg.w["derivado"].set_value("Sí"); dlg._mostrar_derivado_desde(); dlg.update_idletasks()
        self.assertTrue(dlg.w["derivado_procedencia"].winfo_manager())
        self.assertEqual(dlg.w["derivado_procedencia"]["values"][1:], tuple(ai.PROCEDENCIAS))
        dlg.w["derivado"].set_value("No"); dlg._mostrar_derivado_desde()
        self.assertEqual(dlg.w["derivado_procedencia"].get_value(), "")
        # la sección de SSR tiene su viñeta plegable como las demás
        sec = dlg.secciones["ssr"]
        self.assertTrue(sec.abierta)
        sec.plegar(); self.assertFalse(sec.cuerpo.winfo_manager())
        sec.abrir(); self.assertTrue(sec.cuerpo.winfo_manager())
        self.assertEqual(ai.payload({"derivado": "No", "derivado_obs": "x", "dx": []})["derivado_obs"], "")
        dlg.destroy()

    def test_04n_registro_guardado_se_puede_volver_a_ver(self):
        from services import ata as ata_svc
        from services import activityinfo as ai
        from ui.dialog_activityinfo import ActivityInfoDialog
        rec = {"nombre": "Nelly Erunda Romero", "sexo": "M", "fecha": "2026-10-15", "edad_anios": "30", "loc": "Brisas 1",
               "dx1": "PF (ACOs)", "dx2": "Vaginosis", "dx3": "HTA"}
        d = ai.build_defaults(self.db, rec)
        dlg = ActivityInfoDialog(self.root, d, db=self.db)
        dlg.w["consultas"].set_value([ai.CONSULTA_APS, "Salud Sexual y Reproductiva"]); dlg._mostrar_ssr()
        dlg.w["derivado"].set_value("Sí"); dlg._mostrar_derivado_desde()
        dlg.w["derivado_procedencia"].set_value("Institución Estatal"); dlg.w["derivado_obs"].set_value("obs X")
        dlg.w["discapacidad"].set_value("Sí"); dlg._mostrar_disc(); dlg.w["discapacidad_tipo"].set_value(["Mental"])
        dlg.hea.delete("1.0", "end"); dlg.hea.insert("1.0", "HEA escrita a mano")
        dlg.ssr_plan.delete("1.0", "end"); dlg.ssr_plan.insert("1.0", "Plan SSR a mano")
        dlg.w["ssr_menarquia"].set_value("13")
        antes = dlg.snapshot()
        dlg.destroy()
        import json
        self.assertEqual(json.loads(json.dumps(antes)), antes)                   # se puede guardar como JSON
        d2 = ai.build_defaults(self.db, rec)
        d2.update(antes); d2["_restaurado"] = True
        dlg2 = ActivityInfoDialog(self.root, d2, db=self.db)
        despues = dlg2.snapshot()
        dlg2.destroy()
        for k in antes:
            self.assertEqual(despues[k], antes[k], k)
        self.assertEqual(despues["hea"], "HEA escrita a mano")
        self.assertEqual(despues["ssr_plan"], "Plan SSR a mano")
        self.assertEqual(despues["derivado_procedencia"], "Institución Estatal")
        # en la base: se guarda, sobrevive y se lee igual
        db = self.db
        sheet = ata_svc.save_sheet(db, {"fecha": "2026-10-15", "establecimiento": "X", "profesional": "", "codigo": "",
                                        "tipo_establecimiento": "", "departamento": "", "municipio": ""},
                                   [dict({k: "" for k in ata_svc.KEYS}, nombre="Ana Test", sexo="M", numero="1")])
        rid = db.query("SELECT id FROM ata_rows WHERE sheet_id=?", (sheet,))[0]["id"]
        self.assertIsNone(ata_svc.load_datos(db, rid))
        ata_svc.save_datos(db, rid, antes)
        self.assertEqual(ata_svc.load_datos(db, rid), antes)

    def test_04l_valores_por_defecto_de_ssr(self):
        from services import activityinfo as ai
        from ui.dialog_activityinfo import ActivityInfoDialog
        d = ai.build_defaults(self.db, {"nombre": "Ana Pérez López", "sexo": "M", "fecha": "2026-10-15", "edad_anios": "30",
                                        "dx1": "Vaginosis mixta"})
        dlg = ActivityInfoDialog(self.root, d)
        dlg.w["consultas"].set_value([ai.CONSULTA_APS, "Salud Sexual y Reproductiva"])
        dlg._mostrar_ssr()
        self.upd()
        esperado = {"ssr_tipo": "Primera", "ssr_violencia": "No", "ssr_menarquia": "12", "ssr_ritmo": "REGULAR",
                    "ssr_trast_mens": "No", "ssr_menopausia": "No", "ssr_prueba_vph": "No", "ssr_autoex_mamas": "No",
                    "ssr_its": "No", "ssr_itu": "No", "ssr_embarazo_actual": "No", "ssr_embarazo_anterior": "> 2 AÑOS",
                    "ssr_lactancia": "No", "ssr_vph": "No", "ssr_papanicolau": "No", "ssr_examen_mama": "No",
                    "ssr_consejeria": "Si", "ssr_eleg_1": "Preservativo masculino", "ssr_acceso": "Sí",
                    "ssr_va_derivado": "No"}
        for k, v in esperado.items():
            self.assertEqual(dlg.w[k].get_value(), v, k)
        # lo que depende de lo elegido aparece solo
        self.assertEqual(dlg.ssr_met.winfo_manager(), "pack")                      # consejería «Si»: método elegido y acceso
        self.assertEqual(dlg.ssr_ant_obst.winfo_manager(), "pack")                 # embarazo anterior «> 2 años»
        self.assertFalse(dlg.ssr_emb_x.winfo_manager())                           # embarazo actual «No»
        self.assertFalse(dlg.ssr_its_x.winfo_manager())
        # ritmo menstrual: solo REGULAR o IRREGULAR; números obstétricos: lista de 0 a 16
        self.assertEqual(list(dlg.w["ssr_ritmo"]["values"]), ["", "REGULAR", "IRREGULAR"])
        for k in ("gestaciones", "partos", "cesareas", "abortos", "obitos", "hijos_vivos", "hijos_muertos"):
            self.assertEqual(list(dlg.w["ssr_" + k]["values"]), [""] + [str(n) for n in range(17)], k)
            self.assertEqual(dlg.w["ssr_" + k].get_value(), "", k)               # sin valor por defecto: no se llena
        for k, v in {"estado_civil": "Soltero/a"}.items():
            dlg.w[k].set_value(v)
        dlg.w["ssr_gestaciones"].set_value("2"); dlg.w["ssr_partos"].set_value("2")
        dlg._ok()
        r = dlg.result
        self.assertIsNotNone(r)
        s = r["ssr"]
        self.assertEqual((s["tipo"], s["violencia"], s["menarquia"], s["ritmo"], s["trast_mens"], s["menopausia"]),
                         ("Primera", "No", "12", "REGULAR", "No", "No"))
        self.assertEqual((s["prueba_vph"], s["autoex_mamas"], s["its"], s["itu"], s["embarazo_actual"], s["embarazo_anterior"]),
                         ("No", "No", "No", "No", "No", "> 2 AÑOS"))
        self.assertEqual((s["lactancia"], s["vph"], s["papanicolau"], s["examen_mama"], s["consejeria"], s["acceso"], s["va_derivado"]),
                         ("No", "No", "No", "No", "Si", "Sí", "No"))
        self.assertEqual((s["metodos_elegidos"], s["gestaciones"], s["partos"]), (["Preservativo masculino"], "2", "2"))
        self.assertEqual((r["lgtbiq"], r["pueblo"], r["derivado"], r["tipo_consulta"], r["va_derivado"]),
                         ("No", "Ladino / Mestizo", "No", "Primera", "No"))

    def test_04g_vitales_pediatricos(self):
        from services import activityinfo as ai
        from ui.dialog_activityinfo import ActivityInfoDialog
        d = ai.build_defaults(self.db, {"nombre": "Luis Pérez López", "sexo": "H", "fecha": "2026-10-15", "edad_anios": "4",
                                        "dx1": "Fiebre"})
        dlg = ActivityInfoDialog(self.root, d)
        self.upd()
        sis, dia, fc, fr = (int(dlg.w[k].get_value()) for k in ("sistolica", "diastolica", "fc", "fr"))
        self.assertTrue(95 <= sis <= 110 and 60 <= dia <= 75 and 70 <= fc <= 115 and 20 <= fr <= 25, (sis, dia, fc, fr))
        dlg.w["edad"].set_value("8")                                  # pasa a la franja de 6 a 12 años
        dlg._ajustar_vitales()
        sis, dia, fc, fr = (int(dlg.w[k].get_value()) for k in ("sistolica", "diastolica", "fc", "fr"))
        self.assertTrue(100 <= sis <= 120 and 60 <= dia <= 75 and 60 <= fc <= 100 and 14 <= fr <= 22, (sis, dia, fc, fr))
        dlg.w["fc"].set_value("99")                                   # lo escrito a mano no se pisa
        dlg.w["edad"].set_value("14")
        dlg._ajustar_vitales()
        self.assertEqual(dlg.w["fc"].get_value(), "99")
        self.assertTrue(70 <= int(dlg.w["diastolica"].get_value()) <= 80)
        dlg.destroy()

    def test_04h_plan_se_actualiza_y_respeta_lo_editado(self):
        from services import activityinfo as ai
        from ui.dialog_activityinfo import ActivityInfoDialog
        d = ai.build_defaults(self.db, {"nombre": "Ana Pérez López", "sexo": "M", "fecha": "2026-10-15", "edad_anios": "30",
                                        "dx1": "Hipertensión"})
        dlg = ActivityInfoDialog(self.root, d)
        self.upd()
        t1 = dlg.plan.get("1.0", "end").strip()
        self.assertNotEqual(t1, "Plan")
        self.assertRegex(t1, "alarma")
        dlg._regen_plan(True)                                         # «Otra versión»
        self.upd()
        dlg.plan.delete("1.0", "end")
        dlg.plan.insert("1.0", "Mi plan escrito a mano")
        dlg._regen_plan()                                             # lo editado no se pisa
        self.assertEqual(dlg.plan.get("1.0", "end").strip(), "Mi plan escrito a mano")
        dlg._regen_plan(True)
        self.assertNotEqual(dlg.plan.get("1.0", "end").strip(), "Mi plan escrito a mano")
        dlg.destroy()

    def test_04h2_medicamentos_se_agregan_al_plan_de_aps_y_de_ssr(self):
        from services import activityinfo as ai, medicamentos
        from ui.dialog_activityinfo import ActivityInfoDialog
        d = ai.build_defaults(self.db, {"nombre": "Ana Pérez López", "sexo": "M", "fecha": "2026-10-15", "edad_anios": "30",
                                        "dx1": "Vaginosis mixta"})
        dlg = ActivityInfoDialog(self.root, d)
        dlg.w["consultas"].set_value([ai.CONSULTA_APS, "Salud Sexual y Reproductiva"])
        dlg._mostrar_ssr()
        self.upd()
        for k, v in {"estado_civil": "Soltero/a", "escolaridad": "Primaria", "ocupacion": "Estudiante",
                     "discapacidad": "No", "derivado": "No", "tipo_consulta": "Primera"}.items():
            dlg.w[k].set_value(v)
        base_aps = dlg.plan.get("1.0", "end").strip()
        base_ssr = dlg.ssr_plan.get("1.0", "end").strip()
        # se eligen varios, uno tras otro, de la lista
        M = lambda pref: next(t for t in medicamentos.MEDICAMENTOS if t.startswith(pref))  # noqa: E731
        for m in (M("Acetaminofén"), M("Azitromicina 500 mg tableta: 1 Tab"), M("Metronidazol 500 mg tableta: 1 Tab VO c/12")):
            dlg.meds_aps.combo.set_value(m)
            dlg.meds_aps.agregar()
        self.assertEqual(dlg.meds_aps.combo.get_value(), "")            # el selector queda libre para el siguiente
        dlg.meds_aps.combo.set_value("Medicamento escrito a mano 1 Tab VO c/12 horas")   # también se puede escribir otro
        dlg.meds_aps.agregar()
        self.assertEqual(len(dlg.meds_aps.valores()), 4)
        dlg.meds_aps._quitar(dlg.meds_aps._filas[1])                    # se puede quitar uno
        self.assertEqual(len(dlg.meds_aps.valores()), 3)
        dlg.meds_ssr.combo.set_value(M("Metronidazol 500 mg tableta: 1 Tab VO c/12"))
        dlg.meds_ssr.agregar()
        dlg.meds_ssr.combo.set_value(M("Fluconazol"))
        dlg.meds_ssr.agregar()
        # lo escrito en la fila se puede corregir
        dlg.meds_ssr._filas[0][1].set_value("Metronidazol 500 mg tableta: 1 Tab VO c/12 horas por 7 días")
        self.assertEqual(dlg.plan.get("1.0", "end").strip(), base_aps)  # el cuadro del plan no se toca
        self.assertEqual(dlg.ssr_plan.get("1.0", "end").strip(), base_ssr)
        snap = dlg.snapshot()
        dlg._ok()
        r = dlg.result
        self.assertIsNotNone(r)
        self.assertTrue(r["plan"].startswith(base_aps))
        self.assertIn("Medicamentos indicados: Acetaminofén 500 mg tableta: 2 Tab VO c/6 horas por 5 días; ", r["plan"])
        self.assertIn("Medicamento escrito a mano 1 Tab VO c/12 horas.", r["plan"])
        self.assertNotIn("Azitromicina 500 mg tableta: 1 Tab VO c/24", r["plan"])      # el que se quitó
        self.assertTrue(r["ssr"]["plan"].startswith(base_ssr))
        self.assertIn("Metronidazol 500 mg tableta: 1 Tab VO c/12 horas por 7 días; Fluconazol 150 mg tableta: 1 Tab VO dosis única.",
                      r["ssr"]["plan"])
        self.assertNotIn("Fluconazol", r["plan"])                                   # cada plan lleva solo los suyos
        # reabrir la ventana con lo guardado: las listas vuelven y el plan no se duplica
        self.assertEqual(snap["meds_aps"], dlg.meds_aps.valores())
        dlg2 = ActivityInfoDialog(self.root, dict(snap, _restaurado=True))
        self.assertEqual(dlg2.meds_aps.valores(), snap["meds_aps"])
        self.assertEqual(dlg2.meds_ssr.valores(), snap["meds_ssr"])
        self.assertEqual(dlg2.plan.get("1.0", "end").strip(), base_aps)
        dlg2.destroy()
        dlg.destroy()

    def test_04h3_referencia_transfronteriza_siempre_visible_y_no_por_defecto(self):
        from services import activityinfo as ai
        from ui.dialog_activityinfo import ActivityInfoDialog
        d = ai.build_defaults(self.db, {"nombre": "Ana Pérez López", "sexo": "M", "fecha": "2026-10-15", "edad_anios": "30"})
        self.assertEqual(d["transfronteriza"], "No")
        dlg = ActivityInfoDialog(self.root, d)
        self.upd()
        self.assertEqual(dlg.w["va_derivado"].get_value(), "No")
        self.assertEqual(dlg.w["transfronteriza"].get_value(), "No")
        self.assertTrue(dlg.w["transfronteriza"].winfo_ismapped())            # se ve aunque «¿Va a ser derivado?» sea No
        self.assertFalse(dlg.w["n_servicios"].winfo_ismapped())               # esos dos solo con Sí
        self.assertFalse(dlg.w["servicio_brindado"].winfo_ismapped())
        for k, v in {"estado_civil": "Soltero/a", "escolaridad": "Primaria", "ocupacion": "Estudiante",
                     "discapacidad": "No", "derivado": "No", "tipo_consulta": "Primera"}.items():
            dlg.w[k].set_value(v)
        dlg._ok()
        self.assertEqual(dlg.result["transfronteriza"], "No")
        self.assertEqual(ai.payload(dlg.result)["transfronteriza"], "No")      # y se llena en la página
        self.assertEqual(dlg.result["servicio_brindado"], "")
        dlg2 = ActivityInfoDialog(self.root, d)
        dlg2.w["va_derivado"].set_value("Sí")
        dlg2._mostrar_derivacion()
        self.upd()
        for k in ("n_servicios", "transfronteriza", "servicio_brindado"):
            self.assertTrue(dlg2.w[k].winfo_ismapped(), k)
        # el orden en pantalla es el de la página: ¿Va a ser derivado? → ¿A cuántos servicios? → ¿Referencia Transfronteriza?
        ys = [dlg2.w[k].winfo_rooty() for k in ("va_derivado", "n_servicios", "transfronteriza", "servicio_brindado")]
        self.assertEqual(ys, sorted(ys))
        dlg2.w["transfronteriza"].set_value("Sí")
        dlg2.w["va_derivado"].set_value("No")
        dlg2._mostrar_derivacion()
        dlg2.destroy()
        dlg.destroy()

    def test_04h4_hea_de_aps_nunca_lleva_dx_de_ssr(self):
        """Candidiasis vaginal (SSR) + parasitismo (APS): la HEA de APS habla solo del parásito, aunque la consulta de SSR
        no esté marcada y por muchas veces que se pida «Otra versión»; la de SSR habla solo de la candidiasis."""
        import re
        from services import activityinfo as ai
        from ui.dialog_activityinfo import ActivityInfoDialog
        for abrev in ("Candidiasis vaginal", "CVV"):
            d = ai.build_defaults(self.db, {"nombre": "Ana Pérez López", "sexo": "M", "fecha": "2026-10-15",
                                            "edad_anios": "30", "dx1": abrev, "dx2": "Parasitismo"})
            self.assertEqual(d["ssr_dx"][0]["descripcion"], "Candidiasis vulvovaginal", abrev)
            dlg = ActivityInfoDialog(self.root, d)
            self.upd()
            ginec = r"vagin|vulv|flujo|candid|dispareunia|leucorrea"
            self.assertEqual([x for x in dlg._dx_aps_hea() if x], ["Parasitismo"], abrev)
            for i in range(25):
                dlg._regen_hea_aps(True)
                self.assertNotRegex(dlg.hea.get("1.0", "end").lower(), ginec, (abrev, i))
            dlg.w["consultas"].set_value([ai.CONSULTA_APS, "Salud Sexual y Reproductiva"])
            dlg._mostrar_ssr()
            self.upd()
            for i in range(25):
                dlg._regen_hea_aps(True)
                dlg._regen_hea_ssr(True)
                self.assertNotRegex(dlg.hea.get("1.0", "end").lower(), ginec, (abrev, i))
                self.assertRegex(dlg.ssr_hea.get("1.0", "end").lower(), ginec, (abrev, i))
            dlg.destroy()

    def test_04h5_menores_de_18_tienen_estado_civil_escolaridad_y_ocupacion_por_defecto(self):
        from services import activityinfo as ai
        from ui.dialog_activityinfo import ActivityInfoDialog
        base = {"nombre": "Ana Pérez López", "sexo": "M", "fecha": "2026-10-15"}
        for rec in ({"edad_anios": "10"}, {"edad_anios": "17"}, {"edad_anios": "0", "edad_meses": "8"},
                    {"edad_anios": "", "edad_dias": "12"}):
            d = ai.build_defaults(self.db, dict(base, **rec))
            self.assertEqual((d["estado_civil"], d["escolaridad"], d["ocupacion"]), ("No aplica", "Ninguno", "No aplica"), rec)
        for edad in ("18", "30"):
            d = ai.build_defaults(self.db, dict(base, edad_anios=edad))
            self.assertEqual(d["estado_civil"], "Unión Libre", edad)
            self.assertNotEqual((d["escolaridad"], d["ocupacion"]), ("Ninguno", "No aplica"))
        # en la ventana: al corregir la edad se vuelve a proponer, salvo lo que la persona ya cambió
        d = ai.build_defaults(self.db, dict(base, edad_anios="30"))
        dlg = ActivityInfoDialog(self.root, d)
        self.upd()
        self.assertEqual(dlg.w["estado_civil"].get_value(), "Unión Libre")
        dlg.w["edad"].set_value("12")
        dlg._regen_hea(True)
        self.assertEqual([dlg.w[k].get_value() for k in ("estado_civil", "escolaridad", "ocupacion")],
                         ["No aplica", "Ninguno", "No aplica"])
        dlg.w["estado_civil"].set_value("Soltero/a")                       # lo cambió a mano
        dlg.w["edad"].set_value("40")
        dlg._regen_hea(True)
        self.assertEqual(dlg.w["estado_civil"].get_value(), "Soltero/a")   # se respeta
        self.assertNotEqual(dlg.w["escolaridad"].get_value(), "Ninguno")
        self.assertNotEqual(dlg.w["ocupacion"].get_value(), "No aplica")
        dlg.destroy()

    def test_04h6_buscador_de_medicamentos_con_lupa(self):
        from services import activityinfo as ai, medicamentos
        from ui.dialog_activityinfo import ActivityInfoDialog
        d = ai.build_defaults(self.db, {"nombre": "Ana Pérez López", "sexo": "M", "fecha": "2026-10-15", "edad_anios": "30"})
        dlg = ActivityInfoDialog(self.root, d)
        self.upd()
        mp = dlg.meds_aps
        self.assertEqual(mp.buscar(""), [])
        self.assertEqual(mp.buscar("xyzxyz"), [])
        self.assertTrue(all("metronidazol" in m.lower() for m in mp.buscar("METRONIDAZOL")))
        self.assertEqual(len(mp.buscar("metronidazol")), 2)
        self.assertEqual(mp.buscar("acetaminofen"), [m for m in medicamentos.MEDICAMENTOS if m.startswith("Acetaminofén")])  # sin acentos
        self.assertTrue(all("tab" in m.lower() and "500" in m for m in mp.buscar("500 tab")))                  # varias palabras
        self.assertFalse(mp.lista_res.winfo_manager())
        mp.buscador.set_value("metro")                                  # escribir muestra los resultados
        mp._buscar()
        self.upd()
        self.assertEqual(mp.lista_res.winfo_manager(), "pack")
        self.assertEqual(mp.lista_res.size(), 2)                        # las dos de Metronidazol
        mp._agregar_resultado(1)                                        # se toca un resultado: pasa a la lista
        self.assertEqual(len(mp.valores()), 1)
        self.assertTrue(mp.valores()[0].startswith("Metronidazol"))
        self.assertEqual(mp.buscador.get_value(), "")                   # la búsqueda queda libre
        self.assertFalse(mp.lista_res.winfo_manager())
        mp.buscador.set_value("fluco")
        mp._buscar()
        mp._agregar_resultado(0)                                        # Enter agrega el primero
        self.assertEqual(len(mp.valores()), 2)
        mp.buscador.set_value("zzzz")
        mp._buscar()
        self.assertEqual(mp.lista_res.size(), 1)                        # aviso de que no hay coincidencias
        mp._agregar_resultado(0)
        self.assertEqual(len(mp.valores()), 2)                          # y el aviso no se agrega como medicamento
        dlg.destroy()

    def test_04g_hea_de_pf_conserva_el_metodo_del_ata(self):
        """«PF (ACOs)» en SSR: la lista de SSR dice solo «anticoncepción», pero la HEA tiene que hablar de pastillas."""
        import re
        from services import activityinfo as ai
        from ui.dialog_activityinfo import ActivityInfoDialog
        for abrev, quiere, no_quiere in (("PF (ACOs)", r"pastilla|anticonceptivos orales", r"inyec|depo|medroxi|trimestral"),
                                         ("PF (Depo)", r"inyec", r"pastilla|oral")):
            d = ai.build_defaults(self.db, {"nombre": "Nelly Erunda Romero", "sexo": "M", "fecha": "2026-10-15",
                                            "edad_anios": "44", "dx1": abrev, "dx2": "HTA"})
            self.assertRegex(d["ssr_hea"].lower(), quiere, abrev)
            self.assertNotRegex(d["ssr_hea"].lower(), no_quiere, abrev)
            dlg = ActivityInfoDialog(self.root, d)
            dlg.w["consultas"].set_value([ai.CONSULTA_APS, "Salud Sexual y Reproductiva"])
            dlg._mostrar_ssr()
            self.assertIn("anticoncepción", dlg.ssr_rows[0].get_value())          # la lista de SSR no dice el método
            for _ in range(15):                                                   # «Otra versión» tampoco lo pierde
                dlg._regen_hea_ssr(True)
                h = dlg.ssr_hea.get("1.0", "end").lower()
                self.assertRegex(h, quiere, abrev)
                self.assertNotRegex(h, no_quiere, abrev)
                self.assertNotIn("hipertensión", h)                               # la HTA es de APS
            self.assertIn("hipertensión", dlg.hea.get("1.0", "end").lower())
            dlg.destroy()

    def test_04f_seccion_ssr(self):
        from services import activityinfo as ai
        from ui.dialog_activityinfo import ActivityInfoDialog
        d = ai.build_defaults(self.db, {"nombre": "Ana Pérez López", "sexo": "M", "fecha": "2026-10-15", "edad_anios": "30",
                                        "dx1": "Vaginosis mixta", "dx2": "Hipertensión"})
        dlg = ActivityInfoDialog(self.root, d)
        self.assertFalse(dlg.f_ssr.winfo_manager())            # oculta si no se marca SSR
        dlg.w["consultas"].set_value([ai.CONSULTA_APS, "Salud Sexual y Reproductiva"])
        dlg._mostrar_ssr()
        self.assertEqual(dlg.f_ssr.winfo_manager(), "pack")
        self.assertEqual(dlg.w["ssr_ficha"].get_value(), "Larga")
        self.assertEqual(dlg.w["ssr_mismo_punto"].get_value(), "Sí")
        self.assertEqual(len(dlg.ssr_rows), 2)                 # una fila por cada diagnóstico del ATA (mismo formato que APS)
        self.assertIn("Vaginosis bacteriana", dlg.ssr_rows[0].get_value())
        self.assertEqual(dlg.ssr_rows[1].get_value(), "")      # sin equivalente en SSR → vacío
        self.assertFalse(dlg.ssr_der_extra.winfo_manager())
        dlg.w["ssr_va_derivado"].set_value("Sí")
        dlg._mostrar_ssr_der()
        self.assertEqual(dlg.ssr_der_extra.winfo_manager(), "pack")
        # campos que dependen de lo elegido
        # HEA distintas: APS solo con los diagnósticos de APS (hipertensión) y SSR solo con los de SSR (vaginosis)
        h_aps, h_ssr = dlg.hea.get("1.0", "end"), dlg.ssr_hea.get("1.0", "end")
        self.assertIn("hipertensión", h_aps)
        self.assertNotIn("vaginal", h_aps)
        self.assertRegex(h_ssr, r"flujo|secreción")        # (la versión se elige al azar)
        self.assertNotIn("hipertensión", h_ssr)
        self.assertEqual(dlg.ssr_examen.get("1.0", "end").strip(), dlg.examen.get("1.0", "end").strip())   # mismo examen físico
        ex = dlg.ssr_examen.get("1.0", "end")
        self.assertIn("Genitourinario", ex)
        self.assertRegex(ex, "No se realiza inspección genital")                              # vaginosis → hallazgo propio en genitourinario
        self.assertRegex(dlg.ssr_plan.get("1.0", "end"), "alarma")     # plan general según los diagnósticos
        # planes distintos: APS solo con hipertensión (dieta baja en sal), SSR solo con vaginosis (higiene genital)
        pl_aps, pl_ssr = dlg.plan.get("1.0", "end"), dlg.ssr_plan.get("1.0", "end")
        self.assertTrue(pl_ssr.strip().startswith("Se entregan 10 Condones."))   # todo plan de SSR empieza así
        self.assertNotIn("Condones", pl_aps)
        self.assertIn("sal", pl_aps); self.assertNotIn("genital", pl_aps)
        self.assertRegex(pl_ssr, "genital|vaginal|sexual|pareja|preservativo"); self.assertNotIn("sal ", pl_ssr)
        self.assertFalse(dlg.ssr_its_x.winfo_manager())
        self.assertEqual(dlg.ssr_larga.winfo_manager(), "pack")            # ficha larga: menarquía, citología…
        self.assertEqual(dlg._ssr_larga_mujer.winfo_manager(), "pack")
        dlg.w["ssr_menarquia"].set_value("12")
        dlg.w["ssr_its"].set_value("Sí"); dlg.w["ssr_itu"].set_value("Sí"); dlg.w["ssr_violencia"].set_value("Violencia Basada en Género")
        dlg.w["ssr_consejeria"].set_value("Si"); dlg.w["ssr_ya_planifica"].set_value("Sí")
        dlg._ssr_condicionales()
        for fr in (dlg.ssr_its_x, dlg.ssr_itu_x, dlg.ssr_viol_g, dlg.ssr_met, dlg.ssr_actuales):
            self.assertEqual(fr.winfo_manager(), "pack")
        # lista de verificación de embarazo: con consejería «Si» y Mujer CIS / Hombre TRANS
        if dlg.w["genero"].get_value() in ai.LVE_GENEROS:
            self.assertEqual(dlg.ssr_lve.winfo_manager(), "pack")
            dlg._lve_todas("No")
            self.assertIn("No se puede descartar", dlg.ssr_lve_res.cget("text"))
            dlg.w["ssr_lve_abstinencia"].set_value("Sí"); dlg._lve_actualizar()
            self.assertIn("razonablemente seguro", dlg.ssr_lve_res.cget("text"))
        g0 = dlg.w["genero"].get_value()
        dlg.w["genero"].set_value("Hombre CIS"); dlg._ssr_condicionales()
        self.assertFalse(dlg.ssr_lve.winfo_manager())
        dlg.w["genero"].set_value(g0 or "Mujer CIS"); dlg._ssr_condicionales()
        self.assertEqual(dlg.ssr_lve.winfo_manager(), "pack")
        self.assertIn("razonablemente seguro", dlg.ssr_lve_res.cget("text"))
        self.assertFalse(dlg.ssr_viol_o.winfo_manager())
        dlg.w["ssr_its_cual"].set_value("Sífilis")
        dlg.w["ssr_act_1"].set_value("DIU"); dlg.w["ssr_fum"].set_value("2026-08-01"); dlg.w["ssr_embarazo_actual"].set_value("Sí"); dlg.w["ssr_conoce_fum"].set_value("Sí"); dlg._ssr_condicionales()
        for k, v in {"estado_civil": "Soltero/a", "escolaridad": "Primaria", "ocupacion": "Estudiante",
                     "discapacidad": "No", "derivado": "No", "tipo_consulta": "Primera"}.items():
            dlg.w[k].set_value(v)
        dlg._ok()
        r = dlg.result
        self.assertIsNotNone(r)
        self.assertEqual((r["ssr"]["its_cual"], r["ssr"]["metodos_actuales"], r["ssr"]["ya_planifica"], r["ssr"]["embarazo_actual"]),
                         ("Sífilis", ["DIU"], "Sí", "Sí"))
        self.assertEqual(r["ssr"]["fum"], "2026-08-01")
        self.assertEqual(r["ssr"]["menarquia"], "12")
        self.assertEqual(r["ssr"]["lve"]["abstinencia"], "Sí")
        self.assertEqual(len(r["ssr"]["lve"]), 6)
        self.assertNotIn("espermarquia", r["ssr"])
        self.assertEqual(ai.SSR_METODOS_ELEGIDOS[:2], ["Píldora anticonceptiva", "Inyección hormonal / DEPO"])
        self.assertEqual(ai.SSR_METODOS_ELEGIDOS[-2], "Anillo vaginal")
        self.assertEqual(r["ssr"]["dx"][0]["descripcion"], "Vaginosis bacteriana")
        self.assertEqual(r["ssr"]["n_dx"], len(r["ssr"]["dx"]))
        p = ai.payload(r)
        self.assertEqual(p["ssr"]["ficha"], "Larga")
        self.assertFalse([k for k in p if k.startswith("ssr_")])
        self.assertTrue(p["permitir_esta_hecho"])

    def test_04g_calendario_fum(self):
        from datetime import date
        from ui import widgets
        c = widgets.CalendarEntry(self.root)
        c.pack()
        self.assertIsNone(widgets.CalendarEntry.parse("123"))
        self.assertIsNone(widgets.CalendarEntry.parse("2026-02-30"))
        self.assertEqual(widgets.CalendarEntry.parse("2026-08-01"), date(2026, 8, 1))
        c.set_value("2026-08-01")
        c.abrir()
        self.root.update()
        self.assertEqual(c._tit.cget("text"), "agosto 2026")
        c._mover(1)
        self.assertEqual(c._tit.cget("text"), "septiembre 2026")
        c._elegir(date(2026, 9, 15))
        self.assertEqual(c.get_value(), "2026-09-15")
        self.assertIsNone(c._pop)
        c.abrir(); c._elegir(None)
        self.assertEqual(c.get_value(), "")
        c.destroy()

    def test_05_respaldo(self):
        import backup
        db = self.db
        n = db.scalar("SELECT COUNT(*) FROM ata_rows")
        path = backup.create_backup(db)
        db.execute("DELETE FROM ata_rows")
        self.app.show("backup")
        self.answers[:] = ["yes", "ok"]
        self.app.pages["backup"]._restore(str(path))
        self.assertEqual(db.scalar("SELECT COUNT(*) FROM ata_rows"), n)


if __name__ == "__main__":
    unittest.main(verbosity=2)

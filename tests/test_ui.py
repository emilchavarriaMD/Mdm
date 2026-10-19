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

    def test_02_hoja_ata_y_pacientes(self):
        from PIL import Image
        from services import ata as A
        app, db = self.app, self.db
        app.show("ata")
        pg = app.pages["ata"]
        self.upd()
        img = Path(_TMP) / "hoja.png"
        Image.new("RGB", (800, 1000), "white").save(img)
        pg.image_name = A.store_image(img)
        pg._show_image(A.image_path(pg.image_name))
        self.upd()
        self.assertIsNotNone(pg._pil)
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
        self.assertEqual(seen["defaults"]["pueblo"], "")
        self.assertTrue(seen["defaults"]["hea"].startswith("Beneficiario Masc"))
        self.assertEqual(seen["sent"]["estado_civil"], "Soltero/a")
        self.assertEqual(seen["defaults"]["estado_civil"], "")  # lo que el ATA no trae no se inventa
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
        self.assertEqual(self.db.scalar("SELECT COUNT(*) FROM ata_rows"), 2)

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
        self.assertEqual(dlg.ssr_hea.get("1.0", "end").strip(), dlg.hea.get("1.0", "end").strip())   # HEA propia, copia de APS
        self.assertEqual(dlg.ssr_examen.get("1.0", "end").strip(), "Cefalo-caudal")
        self.assertEqual(dlg.ssr_plan.get("1.0", "end").strip(), "Plan")
        self.assertFalse(dlg.ssr_its_x.winfo_manager())
        dlg.w["ssr_its"].set_value("Sí"); dlg.w["ssr_itu"].set_value("Sí"); dlg.w["ssr_violencia"].set_value("Violencia Basada en Género")
        dlg.w["ssr_consejeria"].set_value("Si"); dlg.w["ssr_ya_planifica"].set_value("Sí")
        dlg._ssr_condicionales()
        for fr in (dlg.ssr_its_x, dlg.ssr_itu_x, dlg.ssr_viol_g, dlg.ssr_met, dlg.ssr_actuales):
            self.assertEqual(fr.winfo_manager(), "pack")
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

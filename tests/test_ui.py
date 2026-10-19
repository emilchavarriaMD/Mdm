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
    import backup
    import config
    from database import Database
    from services import patients as P
    from services import visits as V
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
        for name in ("home", "search", "history", "brigades", "reports", "backup", "settings",
                     "patient", "aps", "ssr"):
            self.assertTrue(self.app.show(name))
            self.upd()

    def test_01_formato_de_fecha(self):
        de = widgets.DateEntry(self.root)
        de.var.set("12032026")
        de._on_key(SimpleNamespace(keysym="6", char="6"))
        self.assertEqual(de.get_value(), "12/03/2026")
        de.var.set("1/")
        de._on_key(SimpleNamespace(keysym="slash", char="/"))
        self.assertEqual(de.get_value(), "01/")
        de.set_value("2026-10-05")
        self.assertEqual(de.get_value(), "05/10/2026")

    def test_02_flujo_completo(self):
        app, db = self.app, self.db
        # brigada
        app.show("brigades")
        b = app.pages["brigades"]
        b.new(force=True)
        for k, v in {"codigo": "BR-1", "nombre": "Brigada Prueba", "departamento": "Yoro",
                     "municipio": "El Progreso", "localidad": "Aldea X", "lugar": "Escuela"}.items():
            b.f[k].set_value(v)
        b.f["fecha"].set_value(TODAY)
        self.assertTrue(b.save())
        bid = app.current_brigade_id()
        self.assertIsNotNone(bid)

        # paciente nuevo: la fecha de nacimiento calcula la edad
        app.show("patient", new=True)
        pg = app.pages["patient"]
        for k, v in {"nombres": "María José", "apellidos": "Pérez López", "sexo": "Femenino",
                     "telefono": "9988-7766", "estado_migratorio": "Estado inventado"}.items():
            pg.w[k].set_value(v)
        pg.w["fecha_nacimiento"].set_value("01/01/1990")
        pg._recalc_age()
        self.assertEqual(pg.w["edad_unidad"].get_value(), "años")
        self.assertTrue(pg.w["edad_valor"].get_value().isdigit())
        self.answers[:] = ["stay"]  # tras guardar: "Ver la ficha"
        self.assertTrue(pg.save())
        pid = pg.pid
        self.assertIsNotNone(pid)
        self.assertTrue(pg.locked)  # se abre en modo lectura
        self.assertIn("Estado inventado", db.catalog("estado_migratorio"))  # lista ampliable
        self.assertEqual(db.scalar("SELECT COUNT(*) FROM patients"), 1)

        # duplicado: advierte y no crea si se elige revisar
        app.show("patient", new=True)
        pg = app.pages["patient"]
        for k, v in {"nombres": "Maria Jose", "apellidos": "Perez Lopez", "sexo": "Femenino"}.items():
            pg.w[k].set_value(v)
        pg.w["edad_valor"].set_value("30")
        self.answers[:] = ["cancel"]
        self.assertFalse(pg.save())
        self.assertTrue(any("duplicado" in t.lower() for t, _m, _d in self.log))
        self.assertEqual(db.scalar("SELECT COUNT(*) FROM patients"), 1)
        pg._mark_clean()

        # ---- APS
        app.new_visit("aps", pid)
        self.upd()
        vp = app.pages["aps"]
        self.assertEqual(vp.same_combo.get_value(), "Sí")  # misma fecha que la Ficha Integral
        vp.w["personal"].set_value("Dra. Chávez")
        vp.dx_main.set({"descripcion": "Faringoamigdalitis aguda"})
        vp.w["pas"].set_value("120")
        vp.w["pad"].set_value("80")
        vp._abdomen_limited()
        vp.meds.add_row({"generico": "Amoxicilina", "dosis": "500 mg", "via": "Oral",
                         "cant_prescrita": "21", "cant_entregada": "10", "unidad": "cápsulas"})
        vp.meds.add_row({"generico": "Acetaminofén", "cant_prescrita": "9"})
        self.assertTrue(vp.save(False))
        vid = vp.vid
        v = V.get_visit(db, "aps", vid)
        self.assertEqual(v["main"]["estado"], "borrador")
        self.assertEqual(v["main"]["pas"], 120)
        self.assertIsNone(v["main"]["fc"])  # no se rellenan signos no medidos
        self.assertEqual(v["exam"]["abdomen"]["estado"], V.EXAM_LIMITADO)
        self.assertEqual(v["exam"]["abdomen"]["hallazgos"], V.ABDOMEN_LIMITADO)
        self.assertEqual(v["exam"]["cabeza"]["estado"], V.EXAM_PENDIENTE)  # nada "normal" automático
        self.assertEqual([m["generico"] for m in v["meds"]], ["Amoxicilina", "Acetaminofén"])
        self.assertEqual(v["meds"][0]["cant_prescrita"], 21)
        self.assertEqual(v["meds"][0]["cant_entregada"], 10)
        self.assertIsNone(v["meds"][1]["cant_entregada"])
        self.assertEqual(v["main"]["hea_texto"], "")  # HEA vacía: no se inventa

        # HEA por plantilla: debe revisarse antes de finalizar
        vp.w["hea_motivo"].set_value("Dolor de garganta")
        self.answers[:] = ["yes", "ok"]
        vp.w["hea_texto"].set_value("")
        vp.generate_hea()
        self.assertEqual(vp.hea_origen, "plantilla")
        text = vp.w["hea_texto"].get_value()
        self.assertIn("BORRADOR PRELIMINAR", text)
        self.assertIn("Dolor de garganta", text)
        self.assertIn("PENDIENTES", text.upper())
        self.assertFalse(vp.save(True))  # sin revisión no finaliza
        self.assertTrue(self.errors and "revisada" in " ".join(self.errors[-1]))
        vp.w["hea_revisada"].set_value(True)
        self.answers[:] = ["go"]  # aceptar advertencias
        self.assertTrue(vp.save(True))
        self.assertTrue(vp.locked)
        self.assertEqual(V.get_visit(db, "aps", vid)["main"]["estado"], "finalizada")

        # ---- SSR el mismo día que APS
        app.new_visit("ssr", pid)
        self.upd()
        sp = app.pages["ssr"]
        self.assertEqual(sp.same_combo.get_value(), "Sí")
        sp.w["personal"].set_value("Dra. Chávez")
        sp.w["categoria"].set_value("Planificación familiar")
        sp.w["motivo"].set_value("Desea método anticonceptivo")
        sp.dx_main.set({"descripcion": "Consejería en planificación familiar"})
        sp.tests.add_row({"prueba": "Prueba de embarazo", "estado": "No realizada",
                          "motivo": "No disponible"})
        self.assertTrue(sp.save(False))
        sv = V.get_visit(db, "ssr", sp.vid)
        self.assertEqual(sv["main"]["mismo_dia_aps"], "Sí")
        self.assertTrue(all(i["estado"] == "Pendiente" for i in sv["interventions"].values()))
        self.assertEqual(sv["tests"][0]["estado"], "No realizada")

        # SSR en otra fecha (una atención nueva, sin tocar la APS)
        sp._new_clicked()
        sp.w["fecha_atencion"].set_value("01/01/2020")
        sp._update_same_day()
        self.assertEqual(sp.same_combo.get_value(), "No")
        sp.w["personal"].set_value("Dr. Pérez")
        sp.dx_main.set({"descripcion": "Control"})
        sp.w["categoria"].set_value("Planificación familiar")
        sp.w["motivo"].set_value("Control")
        self.assertTrue(sp.save(False))
        self.assertEqual(db.scalar("SELECT COUNT(*) FROM ssr_visits WHERE patient_id=?", (pid,)), 2)
        self.assertEqual(db.scalar("SELECT COUNT(*) FROM aps_visits WHERE patient_id=?", (pid,)), 1)
        self.assertEqual(db.scalar("SELECT COUNT(*) FROM patients"), 1)

        # cambios sin guardar: pregunta antes de salir
        sp.w["observaciones"].set_value("algo sin guardar")
        self.upd()
        self.answers[:] = ["cancel"]
        self.assertFalse(app.show("home"))
        self.answers[:] = ["discard"]
        self.assertTrue(app.show("home"))

        # PDF de las tres fichas desde la interfaz
        out = Path(_TMP)
        for kind, vid_ in (("aps", vid), ("ssr", sp.vid)):
            page = app.pages[kind]
            page.vid = vid_
            path = out / f"{kind}.pdf"
            page._build_pdf(path)
            self.assertGreater(path.stat().st_size, 1000)

        # historial y búsqueda
        app.show("history", patient_id=pid)
        self.upd()
        self.assertEqual(len(app.pages["history"]._rows), 3)
        app.show("search")
        s = app.pages["search"]
        s.f["texto"].set_value("perez")
        s.search()
        self.assertEqual(len(s._rows), 1)

        # panel
        app.show("home")
        self.assertEqual(app.pages["home"].card["pacientes"][0].cget("text"), "1")

        # copia de seguridad y restauración
        path = backup.create_backup(db)
        db.execute("DELETE FROM ssr_visits")
        self.assertEqual(db.scalar("SELECT COUNT(*) FROM ssr_visits"), 0)
        app.show("backup")
        self.answers[:] = ["yes", "ok"]
        app.pages["backup"]._restore(str(path))
        self.assertEqual(db.scalar("SELECT COUNT(*) FROM ssr_visits"), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)

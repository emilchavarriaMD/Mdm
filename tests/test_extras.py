"""Papelera, alertas de incoherencias, resumen en Excel y bitácora del llenado."""
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
_TMP = tempfile.mkdtemp(prefix="brigadas_extras_")
os.environ["BRIGADAS_DATA_DIR"] = _TMP

from database import Database  # noqa: E402
from services import ata as A  # noqa: E402
from services import coherencia, fill_log, resumen  # noqa: E402

HEADER = {"fecha": "2026-10-13", "establecimiento": "Brisas", "profesional": "Dra", "codigo": "1",
          "tipo_establecimiento": "", "departamento": "Cortés", "municipio": "Choloma"}


def fila(nombre, sexo, anios, dx1="", **kw):
    r = {k: "" for k in A.KEYS}
    r.update(nombre=nombre, sexo=sexo, edad_anios=str(anios), dx1=dx1, cie1="X1", **kw)
    return r


class T20_Extras(unittest.TestCase):
    def setUp(self):
        self.db = Database(Path(tempfile.mkdtemp(dir=_TMP)) / "t.db")
        self.sid = A.save_sheet(self.db, HEADER, [fila("Ana", "M", 34, "HTA"), fila("Luis", "H", 8, "Parasitosis"),
                                                  fila("Rosa", "M", 63, "HTA")])

    def test_papelera_recupera_y_no_pierde_datos(self):
        ids = [r["id"] for r in A.list_records(self.db)]
        A.set_registered(self.db, ids[0], True)
        self.assertEqual(A.delete_records(self.db, ids[:2]), 2)
        self.assertEqual(len(A.list_records(self.db)), 1)
        self.assertEqual(len(A.list_papelera(self.db)), 2)
        # editar la hoja no borra definitivamente lo que está en la papelera
        _sheet, rows = A.get_sheet(self.db, self.sid)
        self.assertEqual(len(rows), 1)
        A.save_sheet(self.db, HEADER, rows, sheet_id=self.sid)
        self.assertEqual(len(A.list_papelera(self.db)), 2)
        self.assertEqual(A.restore_records(self.db, [r["id"] for r in A.list_papelera(self.db)]), 2)
        rec = {r["nombre"]: r for r in A.list_records(self.db)}
        self.assertEqual(set(rec), {"Ana", "Luis", "Rosa"})
        self.assertEqual(rec["Ana"]["ai_estado"], "Pendiente" if rec["Ana"]["ai_estado"] != "Registrado" else "Registrado")

    def test_buscar_por_diagnostico(self):
        self.assertEqual({r["nombre"] for r in A.list_records(self.db, "hta")}, {"Ana", "Rosa"})

    def test_alertas(self):
        self.assertTrue(coherencia.alertas("H", 30, ["Vaginosis mixta"]))
        self.assertTrue(coherencia.alertas("M", 30, ["Hiperplasia prostática"]))
        self.assertTrue(coherencia.alertas("M", 40, ["Control niño sano"]))
        self.assertTrue(coherencia.alertas("M", 5, ["HTA"]))
        self.assertTrue(coherencia.alertas("M", 30, ["Dengue"], "36.5"))
        self.assertEqual(coherencia.alertas("M", 34, ["HTA", "Dermatitis", "Vaginosis mixta"], "36.6"), [])
        self.assertEqual(coherencia.alertas("H", 8, ["Parasitosis intestinal", "Faringitis aguda"]), [])
        self.assertEqual(coherencia.alertas("M", 24, ["PF (ACOs)", "Embarazo"]), [])
        self.assertEqual(coherencia.alertas("M", None, ["HTA"]), [])

    def test_resumen_excel(self):
        from openpyxl import load_workbook
        d = resumen.datos(self.db)
        self.assertEqual(d["total"], 3)
        self.assertEqual(d["sexo"]["M"], 2)
        self.assertEqual(d["dx"][("HTA", "X1")], 2)
        self.assertEqual(d["edades"]["5 a 9 años"], 1)
        out = Path(_TMP) / "res.xlsx"
        self.assertEqual(resumen.exportar(self.db, out), 3)
        wb = load_workbook(out)
        self.assertEqual(wb.sheetnames, ["Resumen", "Diagnósticos", "Pacientes"])
        self.assertEqual(wb["Diagnósticos"]["A2"].value, "HTA")
        self.assertEqual(wb["Pacientes"].max_row, 4)

    def test_bitacora(self):
        p = fill_log.log_path()
        if p.exists():
            p.unlink()
        fill_log.registrar("Ana", {"ficha": ["Perfil: falta"], "aps": [], "ssr": [], "verif": ["«Plan» quedó vacío"]}, None, ["APS"])
        fill_log.registrar("Luis", None, RuntimeError("sin Chrome"), ["APS"])
        e = fill_log.leer()
        self.assertEqual([x["paciente"] for x in e], ["Luis", "Ana"])
        self.assertIn("sin Chrome", fill_log.texto(e[0]))
        self.assertIn("«Plan» quedó vacío", fill_log.texto(e[1]))


if __name__ == "__main__":
    unittest.main()

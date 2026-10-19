import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from services import cie11_catalog as aps
from services import cie11_ssr as ssr


class T_CatalogoSSR(unittest.TestCase):
    def test_tamano_y_unicidad(self):
        self.assertEqual(len(ssr.CATALOG), 105)
        self.assertEqual(len({d for d, _ in ssr.CATALOG}), 105)

    def test_compartidos_con_aps(self):
        compartidos = {d for d, _ in ssr.CATALOG} & {d for d, _ in aps.CATALOG}
        self.assertEqual(len(compartidos), 29)

    def test_sugerencias(self):
        self.assertEqual(ssr.suggest("Vaginosis mixta")[0][1], "MF3A")
        self.assertEqual(ssr.suggest("PF (ACOs)")[0][1], "QA21")
        self.assertEqual(ssr.suggest("Candidiasis vag")[0][1], "1F23.10")
        self.assertEqual(ssr.suggest("zzzz inexistente"), [])

    def test_etiqueta_ida_y_vuelta(self):
        d = "Vaginosis bacteriana"
        self.assertEqual(ssr.from_label(ssr.label(d))[0], d)


if __name__ == "__main__":
    unittest.main()

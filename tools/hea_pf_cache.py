"""Calcula las versiones de HEA de planificación familiar y las guarda en services/hea_pf_cache.py (arranque rápido).
Ejecutar desde la carpeta del programa después de cambiar las piezas de services/hea_pf.py:  python tools/hea_pf_cache.py"""
import os
import pprint
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from services import hea_pf  # noqa: E402

v = {m: hea_pf._armar(m) for m in hea_pf._PIEZAS}
with open(os.path.join(ROOT, "services", "hea_pf_cache.py"), "w", encoding="utf-8") as fh:
    fh.write('"""Versiones de HEA de planificación familiar ya calculadas (generado por tools/hea_pf_cache.py)."""\n')
    fh.write("HUELLA = %r\n" % hea_pf._huella())
    fh.write("VERSIONES = " + pprint.pformat(v, width=140, sort_dicts=False) + "\n")
print({m: len(x) for m, x in v.items()})

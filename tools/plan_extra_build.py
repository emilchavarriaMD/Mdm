"""Une tools/plan_extra/p*.py (frases nuevas del plan) y escribe services/plan_extra_data.py.
Cada índice corresponde a list(plan_data.PLAN). Se descartan frases iguales o casi iguales a las ya existentes."""
import glob, importlib.util, os, pprint, sys
from difflib import SequenceMatcher
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from services.plan_data import PLAN

nombres = list(PLAN)
X = {}
for f in sorted(glob.glob(os.path.join(ROOT, "tools", "plan_extra", "p*.py"))):
    sp = importlib.util.spec_from_file_location("x", f); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    X.update(m.X)

def nuevo(t, pool):
    t = t.strip()
    return all(SequenceMatcher(None, t.lower(), q.lower()).ratio() < 0.9 for q in pool)

GEN_M = ["acudir a los controles programados", "mantener una buena hidratación", "dormir de 7 a 8 horas", "mantener una alimentación balanceada",
         "evitar la automedicación", "evitar el tabaco y el alcohol", "llevar un registro de los síntomas", "realizar actividad física suave según tolerancia",
         "manejar el estrés con técnicas de relajación", "lavarse las manos con frecuencia", "reposar según la necesidad", "llevar los resultados a todas las consultas"]
GEN_A = ["empeoramiento de los síntomas", "fiebre persistente", "dolor intenso que no cede", "dificultad para respirar", "debilidad o mareo intenso"]
out, falta = {}, []
for i, n in enumerate(nombres):
    if i not in X:
        falta.append(i); continue
    ms, as_ = X[i]
    pm, pa = list(PLAN[n]["m"]), list(PLAN[n]["a"])
    nm, na = [], []
    for t in ms:
        if nuevo(t, pm + nm): nm.append(t.strip())
    for t in as_:
        if nuevo(t, pa + na): na.append(t.strip())
    for t in GEN_M:                      # completa hasta 10 medidas y 4 alarmas con frases generales y seguras
        if len(nm) >= 10: break
        if nuevo(t, pm + nm): nm.append(t)
    for t in GEN_A:
        if len(na) >= 4: break
        if nuevo(t, pa + na): na.append(t)
    out[n] = {"m": nm, "a": na}
print("sin extras:", falta)
print("min m", min(len(v["m"]) for v in out.values()), "min a", min(len(v["a"]) for v in out.values()))
for n, v in out.items():
    if len(v["m"]) < 10 or len(v["a"]) < 4:
        print("corto:", n, len(v["m"]), len(v["a"]))
with open(os.path.join(ROOT, "services", "plan_extra_data.py"), "w", encoding="utf-8") as fh:
    fh.write('"""Frases extra del plan (generado por tools/plan_extra_build.py)."""\nEXTRA = ')
    fh.write(pprint.pformat(out, width=140))
    fh.write("\n")

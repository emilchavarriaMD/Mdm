"""Une tools/plan_ssr/{g,s*}.py y escribe services/plan_ssr_data.py (plan propio de la ficha de SSR por diagnóstico)."""
import glob, os, pprint, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from services import cie11_ssr

ns = {}
exec(open(os.path.join(ROOT, "tools", "plan_ssr", "g.py"), encoding="utf-8").read(), ns)
G = ns["G"]
S = {}
for f in sorted(glob.glob(os.path.join(ROOT, "tools", "plan_ssr", "s*.py"))):
    n2 = {}
    exec(open(f, encoding="utf-8").read(), n2)
    S.update(n2["S"])
out = {}
for n in cie11_ssr.descriptions():
    g, m, a = S[n]
    gm, ga = G[g]
    mm = list(dict.fromkeys(m + gm))
    aa = list(dict.fromkeys(a + ga))
    out[n] = {"m": mm, "a": aa}
print("diagnósticos:", len(out), "min m", min(len(v["m"]) for v in out.values()), "min a", min(len(v["a"]) for v in out.values()))
with open(os.path.join(ROOT, "services", "plan_ssr_data.py"), "w", encoding="utf-8") as fh:
    fh.write('"""Plan de la ficha de SSR por diagnóstico (generado por tools/plan_ssr_build.py)."""\nPLAN_SSR = ')
    fh.write(pprint.pformat(out, width=140))
    fh.write("\n")

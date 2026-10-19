"""Exporta el banco de HEA (services/hea_data.py) a un .txt para revisarlo en el Bloc de notas.
Uso: python tools/exportar_banco_hea.py [salida.txt]"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services import cie11_catalog as cat  # noqa: E402
from services.hea_data import ALIAS, BANK  # noqa: E402

PRE = {"F": "Beneficiaria Fem", "M": "Beneficiario Masc", "A": "Beneficiaria/o Fem/Masc"}
TIPO = {"C": "crónico → «antecedente de {t}»", "S": "síntoma → «Además refiere {t}»", "X": "motivo → «Además, {t}»"}


def codigo(n, b):
    for nombre in (ALIAS.get(n), b["n"]):
        if nombre:
            d, c = cat.from_label(nombre)
            if c:
                return c
    return ""


def exportar(salida):
    L = ["BANCO DE HEA — MDm (Médicos del Mundo / COMPASS)",
         f"{len(BANK)} diagnósticos, {sum(len(b['v']) for b in BANK.values())} versiones",
         "=" * 78, "",
         "Cada versión continúa después de «Beneficiaria/o Fem/Masc de X años de edad, que presenta …».",
         "La línea «Al combinar» dice cómo entra ese diagnóstico cuando el paciente tiene 2 o 3 diagnósticos.",
         "Los diagnósticos marcados (no está en ActivityInfo) no tienen opción en la lista del formulario, pero la HEA",
         "sí los incluye cuando vienen en el ATA.", "", "=" * 78]
    lista = {cat.plain(d) for d, _c in cat.CATALOG}
    for n in sorted(BANK):
        b = BANK[n]
        c = codigo(n, b)
        en_ai = cat.plain(ALIAS.get(n, b["n"])) in lista
        L += ["", f"{n}. {b['n']}" + (f"  (CIE-11: {c})" if c else "") + ("" if en_ai else "  (no está en ActivityInfo)"),
              "    Al combinar: " + TIPO[b["k"]].format(t=b["t"])]
        unidad = b["u"]
        for i, v in enumerate(b["v"], 1):
            v = v.strip()
            L.append(f"  V{i}. {PRE.get(b['s'], PRE['A'])} de X {unidad} de edad, que presenta {v}")
    Path(salida).write_text("\r\n".join(L) + "\r\n", encoding="utf-8-sig")
    return len(BANK)


if __name__ == "__main__":
    print(exportar(sys.argv[1] if len(sys.argv) > 1 else "Banco_HEA.txt"), "diagnósticos exportados")

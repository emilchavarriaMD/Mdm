"""Alertas de incoherencias entre sexo, edad, diagnósticos y signos vitales. Solo avisan: nunca cambian nada."""
import re

from services import cie11_catalog as cat

_SOLO_MUJER = re.compile(r"embaraz|gestaci|gestante|puerper|parto|aborto|amenorrea|vagin|vulv|cervic|cuello uterino|"
                         r"leucorrea|dismenorrea|menopaus|mastitis|lactanc|anticoncepci|planificaci[oó]n familiar|"
                         r"\bpf\b|\baco\b|acos|\bdiu\b|prenatal|ovari|uter|candidiasis vulvo|menstru|sangrado uterino", re.I)
_SOLO_HOMBRE = re.compile(r"pr[oó]stat|\bhpb\b|escrot|test[ií]cul|balan|fimosis|prepucio|hidrocele|varicocele|epid[ií]dim", re.I)
_PEDIATRICO = re.compile(r"ni[ñn]o sano|control (del )?ni[ñn]o|crecimiento y desarrollo|lactante|reci[eé]n nacido|"
                         r"\brn\b|bronquiolitis|onfalitis|pa[ñn]al|desnutrici[oó]n aguda", re.I)
_ADULTO = re.compile(r"hipertensi[oó]n|\bhta\b|diabetes|\bdm2?\b|insuficiencia renal|enfermedad renal|\berc\b|epoc|"
                     r"osteoartritis|artrosis|parkinson|cardiopat[ií]a isqu|menopaus|alcohol|tabaqu|"
                     r"hiperplasia prost|\bhpb\b|osteoporosis|embaraz|puerper|anticoncepci|planificaci[oó]n familiar|"
                     r"\bpf\b|\baco", re.I)
_FIEBRE = re.compile(r"fiebre|dengue|chikungunya|zika|faringoamigdalitis bacteriana|neumon[ií]a|pielonefritis|"
                     r"varicela|sarampi[oó]n|celulitis|erisipela", re.I)


def _anios(edad_anios, edad_meses, edad_dias):
    """Edad en años (decimal) a partir de los campos del ATA, o None."""
    def num(x):
        try:
            return float(str(x).strip())
        except (TypeError, ValueError):
            return None
    a, m, d = num(edad_anios), num(edad_meses), num(edad_dias)
    if a is None and m is None and d is None:
        return None
    return (a or 0) + (m or 0) / 12 + (d or 0) / 365


def alertas(sexo, anios, dxs, temperatura=None):
    """Lista de textos cortos con lo que conviene revisar. sexo: 'H' o 'M'; anios: edad en años (decimal) o None."""
    out = []
    for d in dxs or []:
        d = (d or "").strip()
        if not d:
            continue
        n = cat.plain(d)
        if sexo == "H" and _SOLO_MUJER.search(n):
            out.append(f"«{d}» no suele corresponder a un hombre")
        elif sexo == "M" and _SOLO_HOMBRE.search(n):
            out.append(f"«{d}» no suele corresponder a una mujer")
        if anios is not None:
            if anios >= 15 and _PEDIATRICO.search(n):
                out.append(f"«{d}» es un diagnóstico pediátrico y el paciente tiene {_txt(anios)}")
            elif anios < 12 and _ADULTO.search(n) and not (anios >= 10 and re.search(r"anticoncep|planificaci|\bpf\b|embaraz", n)):
                out.append(f"«{d}» es poco común a los {_txt(anios)}")
            elif 10 <= anios < 12 and re.search(r"embaraz|puerper|anticoncep|planificaci|\bpf\b", n):
                out.append(f"«{d}» a los {_txt(anios)}: confirme la edad")
        if temperatura and _FIEBRE.search(n):
            try:
                if float(temperatura) < 37.5:
                    out.append(f"«{d}»: la temperatura anotada es {temperatura} °C (sin fiebre)")
            except ValueError:
                pass
    vistos, res = set(), []
    for x in out:
        if x not in vistos:
            vistos.add(x)
            res.append(x)
    return res


def _txt(anios):
    if anios < 1:
        return f"{round(anios * 12)} meses"
    n = int(anios)
    return f"{n} año" + ("" if n == 1 else "s")


def alertas_registro(r):
    """Alertas de una fila del ATA (list_records / get_record)."""
    return alertas(r.get("sexo"), _anios(r.get("edad_anios"), r.get("edad_meses"), r.get("edad_dias")),
                   [r.get("dx1"), r.get("dx2"), r.get("dx3")])

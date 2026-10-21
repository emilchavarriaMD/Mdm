"""Medicamentos que se pueden agregar al plan (APS y SSR), con la dosis y la frecuencia más usuales para un adulto.

Cada texto queda editable en la ventana: el médico ajusta dosis, frecuencia o días según el caso.
Solo medicamentos: los insumos del listado (jeringas, guantes, gasas, algodón, esparadrapo, yodo povidona,
alcohol, baja lenguas, curitas, toallitas, prueba de embarazo) no se recetan y no están aquí.
"""

# (texto completo que se escribe en el plan); más abajo se ordena alfabéticamente para la lista desplegable.
_LISTA = [
    # analgésicos, antiinflamatorios, relajantes
    "Acetaminofén 500 mg tableta: 2 Tab VO c/6 horas por 5 días",
    "Ibuprofeno 600 mg tableta: 1 Tab VO c/8 horas por 5 días",
    "Diclofenaco 75 mg ampolla: 1 Amp IM dosis única",
    "Metocarbamol 500 mg tableta: 1 Tab VO c/8 horas por 5 días",
    "Hioscina 10 mg tableta: 1 Tab VO c/8 horas por 3 días",
    # antibióticos
    "Amoxicilina 500 mg cápsula: 1 Cap VO c/8 horas por 7 días",
    "Azitromicina 500 mg tableta: 1 Tab VO c/24 horas por 3 días",
    "Azitromicina 500 mg tableta: 2 Tab VO dosis única",
    "Ciprofloxacina 500 mg tableta: 1 Tab VO c/12 horas por 7 días",
    "Trimetoprim sulfametoxazol 160/800 mg tableta: 1 Tab VO c/12 horas por 5 días",
    "Cefixima 400 mg tableta: 1 Tab VO c/24 horas por 7 días",
    "Cefixima 400 mg tableta: 1 Tab VO dosis única",
    "Doxiciclina 100 mg tableta: 1 Tab VO c/12 horas por 7 días",
    "Ciprofloxacina + hidrocortisona + lidocaína gotas óticas: 4 gotas en el oído afectado c/12 horas por 7 días",
    # antiparasitarios, antimicóticos, antiprotozoarios
    "Albendazol 200 mg tableta: 2 Tab VO dosis única",
    "Metronidazol 500 mg tableta: 1 Tab VO c/8 horas por 7 días",
    "Metronidazol 500 mg tableta: 1 Tab VO c/12 horas por 7 días",
    "Tinidazol 500 mg tableta: 4 Tab VO dosis única",
    "Fluconazol 150 mg tableta: 1 Tab VO dosis única",
    "Ketoconazol 2% crema: aplicar en la zona afectada c/24 horas por 14 días",
    "Clotrimazol 500 mg óvulo vaginal: 1 Óvulo vaginal por la noche dosis única",
    "Clindamicina 2 g / Clotrimazol 2 g óvulos vaginales: 1 Óvulo vaginal por la noche por 3 días",
    # alergia, tos, resfriado
    "Loratadina 10 mg tableta: 1 Tab VO c/24 horas por 7 días",
    "Difenhidramina 50 mg tableta: 1 Tab VO c/8 horas por 3 días",
    "Dextrometorfano + clorfenamina jarabe antitusivo: 10 mL VO c/8 horas por 5 días",
    "Salbutamol 100 mcg inhalador: 2 Puff inhalados c/6 horas por 5 días",
    "Beclometasona 250 mcg inhalador: 1 Puff inhalado c/12 horas por 30 días (enjuagar la boca después)",
    # corticoides
    "Prednisona 5 mg tableta: 4 Tab VO c/24 horas por 5 días",
    "Dexametasona 8 mg ampolla: 1 Amp IM dosis única",
    "Hidrocortisona 1% crema: aplicar en la zona afectada c/12 horas por 7 días",
    # digestivo
    "Lansoprazol 30 mg tableta: 1 Tab VO c/24 horas en ayunas por 14 días",
    "Hidróxido de aluminio + hidróxido de magnesio (antiácido) tableta: 1 Tab masticable VO c/8 horas después de las comidas por 5 días",
    "Hidróxido de aluminio + hidróxido de magnesio (antiácido) jarabe: 10 mL VO c/8 horas después de las comidas por 5 días",
    "Metoclopramida 10 mg tableta: 1 Tab VO c/8 horas antes de las comidas por 3 días",
    "Loperamida 2 mg tableta: 2 Tab VO la primera dosis y luego 1 Tab tras cada evacuación líquida (máximo 8 Tab al día) por 2 días",
    "Sales de rehidratación oral sobre: 1 Sobre en 1 litro de agua, tomar a sorbos tras cada evacuación líquida, por 3 días",
    "Benzocaína + hidrocortisona (crema antihemorroidal): aplicar en la zona c/12 horas por 7 días",
    # vitaminas
    "Multivitaminas para adulto tableta: 1 Tab VO c/24 horas por 30 días",
    "Ácido fólico 5 mg tableta: 1 Tab VO c/24 horas por 30 días",
    # planificación familiar
    "Anticonceptivo oral combinado (ciclo de 28 tabletas): 1 Tab VO c/24 horas a la misma hora, iniciar el primer día de la menstruación, por 28 días",
    "Medroxiprogesterona 150 mg ampolla: 1 Amp IM cada 3 meses",
    "Levonorgestrel 1.5 mg (PAE): 1 Tab VO dosis única lo antes posible, dentro de las primeras 72 horas",
]


def _clave(texto):
    """Para ordenar sin que los acentos ni las mayúsculas cambien el orden."""
    import unicodedata
    return unicodedata.normalize("NFD", texto).encode("ascii", "ignore").decode().lower()


# La lista desplegable va en orden alfabético (de la A a la Z por el nombre del medicamento).
MEDICAMENTOS = sorted(_LISTA, key=_clave)


def nombre(texto):
    """Solo el nombre y la presentación, sin la indicación (lo que va antes de los dos puntos)."""
    return texto.split(":", 1)[0].strip()


def formatear(lineas):
    """Texto que se añade al final del plan. Vacío si no hay medicamentos."""
    lineas = [l.strip().rstrip(".;") for l in lineas if l and l.strip()]
    if not lineas:
        return ""
    return "Medicamentos indicados: " + "; ".join(lineas) + "."


def agregar_al_plan(plan, lineas):
    """Plan + medicamentos, sin alterar el texto del plan. Si el plan ya los trae (registro reabierto), no los repite."""
    extra = formatear(lineas)
    base = (plan or "").strip()
    if not extra:
        return base
    if extra in base:
        return base
    return (base + "\n" + extra).strip()

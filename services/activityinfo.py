"""Registro de un paciente del ATA en ActivityInfo.

Se abre Chrome (con un perfil propio del programa), se abre el formulario «newRecord» y se LLENAN
los campos. El programa NUNCA guarda: no pulsa «Guardar registro», «Guardar como borrador» ni
«Está hecho». La ficha la crea la persona a mano, después de revisar los datos.
Tampoco escribe contraseñas: si ActivityInfo pide iniciar sesión, la persona lo hace en la ventana.
"""
import random
import re
import sys
import time
import webbrowser
from pathlib import Path

import config
from services import cie11_catalog as cat
from services import cie11_ssr
from services import ata as _ata
from services import hea_banco
from services.hea import generate_hea

FORM_URL = "https://www.activityinfo.org/app#form/cgagdtzm4cnphz5kmo/newRecord"

GENEROS = ["Hombre CIS", "Mujer CIS", "Hombre TRANS", "Mujer TRANS", "No binario"]
ESTADOS_CIVILES = ["Casado/a", "Divorciado/a", "Soltero/a", "Unión Libre", "Viudo/a",
                   "Prefiere no contestar", "No aplica"]
ESCOLARIDADES = ["Preescolar", "Primaria", "Secundaria/Bachillerato", "Formación Técnica",
                 "Universitaria", "Posgrado", "Prefiere no contestar", "Ninguno"]
OCUPACIONES = ["Comercio informal", "Construcción", "Cuidador/a", "Desempleado/a", "Estudiante",
               "Funcionario/a público", "No relevante", "Persona en situación de prostitución", "Servicios",
               "Trabajador/a de la salud", "Trabajo académico", "Trabajo agrícola",
               "Trabajo doméstico NO remunerado", "Trabajo doméstico remunerado", "Trabajo industrial",
               "Transporte", "Otro", "No aplica"]
PERFILES = ["Persona en tránsito", "Población desplazada interna", "Persona refugiada",
            "Niño, niña o adolescente (NNA)", "Persona retornada", "Solicitante de asilo",
            "Sobreviviente de violencia de género", "OSV (Otras situaciones de violencia)",
            "Persona en riesgo de desplazamiento", "Comunidad de acogida",
            "Migrante en proceso de retorno", "Líder/esa comunitario/a"]
PERFIL_FIJO = "Persona en riesgo de desplazamiento"
LGTBIQ = ["Sí", "No"]
PUEBLOS = ["Afrodescendiente / Creole / Afromestizo", "Extranjero", "Garífuna", "Ladino / Mestizo", "Maya",
           "Xinca", "No responde", "Lenca", "Miskito", "Tolupán", "Pech", "Tawanhka"]
DISCAPACIDAD = ["Sí", "No", "Prefiere no contestar"]
TIPOS_DISCAPACIDAD = ["Física o motora", "Intelectual", "Mental", "Sensorial"]   # «¿Qué tipo de discapacidad?» (sale si es Sí)
# Signos vitales: listas desplegables de la ventana de registro y valores iniciales.
LISTA_SISTOLICA = [str(x) for x in range(60, 251, 10)]
LISTA_DIASTOLICA = [str(x) for x in range(30, 151, 10)]
LISTA_FC = [str(x) for x in range(40, 201)]
LISTA_FR = [str(x) for x in range(10, 51)]
# Temperatura: primero los grados enteros (35 a 41) y después los décimos (35.1 a 40.9); lo habitual es SIN decimales.
LISTA_TEMP = [str(x) for x in range(35, 42)] + [f"{x / 10:.1f}" for x in range(350, 411) if x % 10]


# Valores normales en pediatría por edad (meses de edad desde, hasta sin incluir): sistólica, diastólica, FC, FR
VITALES_PEDIATRIA = [
    (0, 3, (65, 85), (45, 55), (110, 160), (30, 60)),
    (3, 6, (70, 90), (50, 65), (100, 150), (30, 45)),
    (6, 12, (80, 100), (55, 65), (90, 130), (25, 40)),
    (12, 36, (90, 105), (55, 70), (80, 125), (20, 30)),
    (36, 72, (95, 110), (60, 75), (70, 115), (20, 25)),
    (72, 144, (100, 120), (60, 75), (60, 100), (14, 22)),
    (144, 216, (100, 120), (70, 80), (60, 100), (12, 18)),
]


def edad_en_meses(edad, unidad="años"):
    """Edad en meses, o None si no se sabe. Los días cuentan como recién nacido (0 meses)."""
    try:
        n = int(str(edad).strip())
    except ValueError:
        return None
    u = (unidad or "años").lower()
    return n * 12 if u.startswith("a") else n if u.startswith("m") else 0


def grupo_vitales(sexo, edad, unidad="años"):
    """Grupo de valores de referencia (cambia solo al pasar a otra franja de edad o de sexo)."""
    m = edad_en_meses(edad, unidad)
    if m is None:
        return ("sin_edad", sexo)
    for i, (lo, hi, *_r) in enumerate(VITALES_PEDIATRIA):
        if lo <= m < hi:
            return ("ped", i)
    return ("adulto", sexo)


def es_hta(texto):
    """¿El diagnóstico es hipertensión arterial (HTA)? No cuenta la del embarazo (gestacional, preeclampsia…)."""
    p = " ".join(cat.plain(texto).split())
    if not p or re.search(r"gestacional|embarazo|preeclampsia|eclampsia|pulmonar|ocular|portal", p):
        return False
    return bool(re.search(r"\bhta\b|hipertension", p))


def vitales_defecto(sexo, edad, unidad="años", rng=None, hta=False):
    """Valores iniciales de los signos vitales (la persona los cambia en la lista). En menores de 18 años se eligen al
    azar dentro del rango normal para su edad; en adultos, valores habituales; con HTA (adultos): sistólica 140 o 130 y
    diastólica 90 u 80. La temperatura es 36 o 37, SIN decimales. Si no se sabe la edad, la frecuencia respiratoria
    queda vacía."""
    rng = rng or random
    temp = str(rng.choice([36, 37]))
    g = grupo_vitales(sexo, edad, unidad)
    if g[0] == "ped":
        _lo, _hi, sis, dia, fc, fr = VITALES_PEDIATRIA[g[1]]
        return {"sistolica": str(rng.randint(*sis)), "diastolica": str(rng.randint(*dia)),
                "fc": str(rng.randint(*fc)), "fr": str(rng.randint(*fr)), "temperatura": temp}
    sis, dia = ("120", "70" if sexo == "M" else "80")
    if hta:
        sis, dia = str(rng.choice([140, 130])), str(rng.choice([90, 80]))
    return {"sistolica": sis, "diastolica": dia,
            "fc": str(rng.randint(65, 90)), "fr": str(rng.randint(12, 20)) if g[0] == "adulto" else "",
            "temperatura": temp}


# Derivación (hacia) / Servicio brindado: «recapitulativo interno MdM para todas las atenciones».
VA_DERIVADO = ["Sí", "No"]
PROCEDENCIAS = ["Establecimiento público de salud", "Institución Estatal", "MdM Atención primária", "MdM Gestión de casos",
                "MdM Salud mental y apoyo psicosocial", "Mdm Salud sexual y reproductiva", "MdM Técnicos de campo",
                "Organización de la Sociedad Civil", "Organización Internacional", "MdM Nutrición"]   # «Procedencia de la derivación»
N_SERVICIOS = ["Un servicio", "Dos servicios"]
SERVICIOS_BRINDADOS = ["Protección", "Salud", "Recuperación económica/medios de vida", "Justicia/Asistencia legal",
                       "Gestión de casos MdM", "Educación NNA"]
SERVICIOS_SALUD = ["MdM - Atención primaria", "MdM - Salud sexual y reproductiva",
                   "MdM - Salud mental y apoyo psicosocial", "Consulta externa especializada publico",
                   "Atención hospitalaria (de emergencia o no)", "Atención primaria-establecimiento de salud local",
                   "Médico especialista privado", "Otras organizaciones con servicios de salud"]
PLAN_BASE = "Plan"
PLAN_SSR_INICIO = "Se entregan 10 Condones."   # todo plan de SSR empieza así; sigue el plan del banco

# Salud Sexual y Reproductiva (subformulario SSR de la ficha integral)
TIPOS_SSR = ["Primera", "Reconsulta", "Seguimiento"]
SSR_FICHAS = ["Corta", "Larga"]
SI_NO = ["Sí", "No"]
# Lista de verificación de embarazo (SSR): sale con consejería «Si» y género Mujer CIS u Hombre TRANS.
# (clave, rótulo exacto en ActivityInfo, pregunta corta para la ventana)
LVE_PREGUNTAS = [
    ("menstruacion", "1. Menstruación", "¿La menstruación comenzó en los últimos 7 días (12 días si quiere DIU de cobre)?"),
    ("abstinencia", "2. Abstinencia sexual", "¿Abstinencia sexual desde la última menstruación, parto, cesárea o aborto?"),
    ("metodo", "3. Metodo anticonceptvo desde última menstruación",
     "¿Usa un método fiable de forma consistente y correcta desde la última menstruación, parto, cesárea o aborto?"),
    ("bebe4", "4. Bebé en las últimas 4 semanas", "¿Tuvo un bebé en las últimas 4 semanas?"),
    ("bebe6", "5. Bebé de menos de 6 meses",
     "¿Bebé de menos de 6 meses con lactancia exclusiva (o casi) y sin menstruación desde el parto?"),
    ("aborto", "6. Aborto en los últimos días", "¿Tuvo un aborto en los últimos 7 días (12 días si quiere DIU de cobre)?"),
]
LVE_GENEROS = ("Mujer CIS", "Hombre TRANS")


def lve_resultado(resp: dict) -> str:
    """Lo mismo que calcula ActivityInfo: todas «No» → no se descarta embarazo; alguna «Sí» → razonablemente seguro."""
    vals = [resp.get(k, "") for k, _, _ in LVE_PREGUNTAS]
    if any(v == "Sí" for v in vals):
        return "Se puede estar razonablemente seguro/a de que no está embarazada y empezar método anticonceptivo"
    if all(v == "No" for v in vals):
        return "No se puede descartar embarazo, es necesario descartarlo mediante otro método"
    return ""
SSR_MAX_DX = 2
SSR_VIOLENCIA = ["No", "Violencia Basada en Género", "Otra Situación de Violencia"]
SSR_SI_NO_NS = ["Sí", "No", "No sabe"]
SSR_VIOLENCIA_GENERO = ["Violencia física", "Violencia psicológica", "Violencia sexual", "Violencia económica",
                        "Violencia patrimonial", "Violencia institucional", "Unión Temprana", "Matrimonio Forzado"]
SSR_VIOLENCIA_OTRAS = ["Desórdenes civiles", "Disturbios internos", "Represión Estatal", "Violencia electoral",
                       "Violencia de maras, pandillas y/o crimen organizado", "Amenazas de muerte", "Extorsión",
                       "Reclutamiento forzado", "Despojo de tierras", "Expulsión de vivienda", "Usurpación de propiedad",
                       "Discriminación", "Delincuencia organizada y urbana", "Deportación forzada"]
# Ordenados por frecuencia de uso en consulta (los más usados primero; los casi sin uso, al final)
SSR_METODOS_ELEGIDOS = ["Píldora anticonceptiva", "Inyección hormonal / DEPO", "Preservativo masculino",
                        "Ligadura de trompas / Vasectomía", "Implante subdérmico", "DIU", "Píldora del dia después",
                        "Métodos naturales (calendário, muco, coitus interruptus, temperatura)", "Preservativo feminino",
                        "Diafragma", "Espermicida", "Esponja", "Anillo vaginal", "Ninguno"]
SSR_METODOS_ACTUALES = SSR_METODOS_ELEGIDOS[:-1] + ["Otro (no convencional)"]
SSR_EMBARAZO_ANTERIOR = ["> 2 AÑOS", "< 2 AÑOS", "No hubo embarazo"]
SSR_RITMOS = ["REGULAR", "IRREGULAR"]                 # en mayúsculas, como se escribe en ActivityInfo
SSR_NUMEROS = [str(n) for n in range(0, 17)]          # gestaciones, partos, cesáreas, abortos, óbitos, hijos vivos/muertos
SSR_VACUNAS = ["Td (toxoide tetánico)", "VPH (VIRUS PAPILOMA HUMANO)", "HEPATITIS B:", "SRP (SARAMPIÓN-RUBEOLA):"]
SSR_SERVICIO_SALUD = "MdM-Salud sexual y reproductiva"
SSR_SERVICIOS_SALUD = ["MdM - Atención primaria", "MdM-Salud sexual y reproductiva", "MdM-Salud mental y apoyo psicosocial",
                       "MdM - Seguimiento telefónico", "Consulta externa especializada publico",
                       "Atención hospitalaria (de emergencia o no)", "Atención primaria-establecimiento de salud local",
                       "Médico especialista privado", "Otras organizaciones con servicios de salud"]                      # «Número de diagnósticos» del SSR solo admite 1 o 2
# La persona permitió que el programa pulse «Está hecho» SOLO en el subformulario de Atención primaria (cuando el paciente
# lleva también SSR) para volver a la ficha y abrir el de SSR. Nunca se pulsa «Guardar registro» ni «Guardar como borrador».
PERMITIR_ESTA_HECHO_EN_APS = True

# Texto inicial de «Examen Físico» (después habrá una biblioteca de exámenes). La talla no se toma ni se llena.
from services import examen_fisico as _exa
EXAMEN_FISICO_APS = _exa.compose([], ssr=False)
EXAMEN_FISICO_SSR = _exa.compose([], ssr=True)
EXAMEN_FISICO_BASE = EXAMEN_FISICO_APS

DERIVADO = ["Sí", "No"]
TIPOS_CONSULTA = ["Primera", "Reconsulta", "Seguimiento", "Tamizaje de signos vitales",
                  "Nuevo motivo de consulta", "Procedimiento terapéutico no quirúrgico"]
CONSULTA_APS = "Atención Primaria de Salud"
CONSULTAS = [CONSULTA_APS, "Salud Sexual y Reproductiva", "Salud Mental y Apoyo Psícosocial",
             "Gestión de casos de VdG", "Nutrición", "Wash"]
# Campos obligatorios del formulario que el ATA no trae: se avisa si quedan vacíos.
OBLIGATORIOS = [("estado_civil", "Estado civil"), ("escolaridad", "Grado de escolaridad"),
                ("ocupacion", "Sector de ocupación"), ("discapacidad", "¿Tiene alguna discapacidad?"),
                ("derivado", "¿Ha sido derivado/a?")]

# Valores fijos que se configuran una vez (pantalla Configuración).
SETTINGS = [
    ("ai_lugar", "Lugar de atención (al elegirlo se llenan País y Departamento)", "San Pedro Sula"),
    ("ai_donante", "Proyecto: Donante Nombre", "ECHO"),
    ("ai_proyecto", "Proyecto: Título del proyecto", "ECHO - COMPASS"),
    ("ai_perfin", "Proyecto: PERFIN", "F09010020"),
    ("ai_nacionalidad", "País de nacionalidad", "Honduras"),
    ("ai_idioma", "Idioma", "Español"),
    ("ai_profesional", "Profesional que atiende (APS)", "Nadia Alejandra Chavarría López"),
]

_driver = None


# -- datos --------------------------------------------------------------------------

def split_name(full: str):
    """Separa «nombres» y «apellidos» como punto de partida (la persona lo corrige en la ventana).
    4 o más palabras: 2 nombres + el resto; 3: 1 nombre + 2 apellidos; 2: 1 + 1."""
    parts = (full or "").split()
    if len(parts) >= 4:
        return " ".join(parts[:2]), " ".join(parts[2:])
    if len(parts) == 3:
        return parts[0], " ".join(parts[1:])
    if len(parts) == 2:
        return parts[0], parts[1]
    return (parts[0] if parts else ""), ""


def get_setting_values(db):
    return {k: (db.get_setting(k, default) or default) for k, _l, default in SETTINGS}


def dx_map(db):
    return {r["abrev"].strip().lower(): r for r in db.query("SELECT * FROM dx_map")}


def list_dx_map(db):
    return db.query("SELECT * FROM dx_map ORDER BY abrev COLLATE NOCASE")


def save_dx_map(db, abrev, descripcion, cie11):
    abrev = (abrev or "").strip()
    if not abrev:
        raise ValueError("Escriba la abreviatura tal como aparece en el ATA (por ejemplo: HTA).")
    db.execute("INSERT INTO dx_map (abrev, descripcion, cie11) VALUES (?,?,?) "
               "ON CONFLICT(abrev) DO UPDATE SET descripcion=excluded.descripcion, cie11=excluded.cie11",
               (abrev, (descripcion or "").strip(), (cie11 or "").strip()))


def delete_dx_map(db, abrev):
    db.execute("DELETE FROM dx_map WHERE abrev=?", (abrev,))


def es_menor_de_edad(edad, unidad="años"):
    """Menor de 18 años: lo que está en meses o días siempre lo es; en años, de 0 a 17. Sin edad: False."""
    if str(unidad or "").lower() in ("meses", "días", "dias"):
        return True
    e = str(edad or "").strip()
    return e.isdigit() and int(e) < 18


def defectos_ficha(rng=None, menor=False, estado_civil="", ocupacion=""):
    """Valores que se proponen en la ficha cuando el ATA no los trae (la persona los cambia en la ventana).
    Escolaridad y sector de ocupación se eligen al azar entre dos opciones. En menores de 18 años:
    estado civil «No aplica», escolaridad «Ninguno» y sector de ocupación «No aplica»."""
    rng = rng or random
    d = {"lgtbiq": "No", "pueblo": "Ladino / Mestizo", "estado_civil": "Unión Libre",
         "escolaridad": rng.choice(["Primaria", "Secundaria/Bachillerato"]),
         "ocupacion": rng.choice(["Trabajo doméstico NO remunerado", "Otro"]),
         "discapacidad": "No", "derivado": "No"}
    if menor:
        d.update(estado_civil="No aplica", escolaridad="Ninguno", ocupacion="No aplica")
    else:                                   # lo que dice el ATA (estado civil, profesión) manda sobre el valor por defecto
        d.update({k: v for k, v in (("estado_civil", estado_civil), ("ocupacion", ocupacion)) if v})
    return d


LUGARES_ATENCION = ["San Pedro Sula", "Choloma"]      # «Lugar de atención» (Cortés): depende de lo que diga el ATA


def lugar_atencion(rec: dict, por_defecto: str = "San Pedro Sula") -> str:
    """Choloma o San Pedro Sula según el ATA: el municipio del encabezado de la hoja (siempre es uno de los dos);
    si falta, el establecimiento y luego el municipio del paciente; si no dice ninguno, el valor de Configuración."""
    for campo in ("mun_hoja", "establecimiento", "mun", "loc"):
        t = cat.plain(str(rec.get(campo) or ""))
        if "choloma" in t:
            return "Choloma"
        if "san pedro" in t or t.strip() in ("sps", "s p s"):
            return "San Pedro Sula"
    return por_defecto


def defectos_ssr():
    """Valores que se proponen en Salud Sexual y Reproductiva (antecedentes, obstétricos, anticoncepción, derivación)."""
    return {"ssr_violencia": "No", "ssr_menarquia": "12", "ssr_ritmo": SSR_RITMOS[0],
            "ssr_trast_mens": "No", "ssr_menopausia": "No", "ssr_prueba_vph": "No", "ssr_autoex_mamas": "No",
            "ssr_its": "No", "ssr_itu": "No",
            "ssr_embarazo_actual": "No", "ssr_embarazo_anterior": SSR_EMBARAZO_ANTERIOR[0], "ssr_lactancia": "No",
            "ssr_vph": "No", "ssr_papanicolau": "No", "ssr_examen_mama": "No",
            "ssr_victima_sexual": "No", "ssr_consejeria": "Si", "ssr_eleg_1": "Preservativo masculino", "ssr_acceso": "Sí"}


def defectos_obstetricos(rec: dict) -> dict:
    """Gestas, partos, cesáreas, abortos, hijos vivos y muertos escritos en el ATA (columna G=  P=  C=  A=  HV=  HM=)."""
    from services import ata as ata_svc
    d = ata_svc.parse_obst(rec.get("obst"))
    if not d:
        return {}
    clave = {"G": "ssr_gestaciones", "P": "ssr_partos", "C": "ssr_cesareas", "A": "ssr_abortos",
             "HV": "ssr_hijos_vivos", "HM": "ssr_hijos_muertos"}
    out = {clave[k]: str(min(v, 16)) for k, v in d.items()}      # las listas de ActivityInfo llegan hasta 16
    if d.get("G") == 0:
        out["ssr_embarazo_anterior"] = "No hubo embarazo"
    return out


def telefono_internacional(texto) -> str:
    """Teléfono del ATA con prefijo internacional (Honduras +504 si trae solo 8 dígitos). Vacío si no hay número."""
    raw = (texto or "").strip()
    d = re.sub(r"\D", "", raw)
    if not d:
        return ""
    if raw.startswith("+") or raw.startswith("00"):
        return "+" + (d[2:] if raw.startswith("00") else d)
    if len(d) == 8:
        return "+504" + d
    if d.startswith("504") and len(d) == 11:
        return "+" + d
    return raw


def build_defaults(db, rec: dict) -> dict:
    """Datos iniciales para la ventana de revisión. Lo que está en el ATA se toma del ATA; lo que el ATA no trae
    (estado civil, escolaridad, antecedentes de SSR…) se propone con valores por defecto que la persona corrige."""
    st = get_setting_values(db)
    nombres, apellidos = split_name(rec.get("nombre"))
    sexo = (rec.get("sexo") or "").upper()
    genero = {"M": "Mujer CIS", "H": "Hombre CIS"}.get(sexo, "")
    anios = (rec.get("edad_anios") or "").strip()
    edad = anios or ("0" if (rec.get("edad_meses") or rec.get("edad_dias")) else "")
    dxmap = dx_map(db)
    dxs = []
    for i in (1, 2, 3):
        txt = (rec.get(f"dx{i}") or "").strip()
        if not txt:
            continue
        m = dxmap.get(txt.lower())
        cie = (rec.get(f"cie{i}") or "").strip()
        dxs.append({"abrev": txt, "descripcion": m["descripcion"] if m else "",
                    "cie11": (m["cie11"] if m else "") or cie})
    desc = {k: v["descripcion"] for k, v in dxmap.items() if v["descripcion"]}
    meses = (rec.get("edad_meses") or "").strip()
    dias = (rec.get("edad_dias") or "").strip()
    if anios and anios != "0":
        persona = {"sexo": sexo, "edad": anios, "unidad": "años"}
    elif meses:
        persona = {"sexo": sexo, "edad": meses, "unidad": "meses"}
    elif dias:
        persona = {"sexo": sexo, "edad": dias, "unidad": "días"}
    elif anios == "0":
        persona = {"sexo": sexo, "edad": "0", "unidad": "años"}      # «0 años» es un menor de un año, no una edad vacía
    else:
        from services.patients import calc_age
        nac = calc_age((rec.get("fecha_nacimiento") or "")[:10], (rec.get("fecha") or "")[:10] or None)
        if nac:                                                       # sin edad escrita: se calcula con la fecha de nacimiento
            persona = {"sexo": sexo, "edad": str(nac[0]), "unidad": nac[1]}
            if not edad:
                edad = str(nac[0]) if nac[1] == "años" else "0"
        else:
            persona = {"sexo": sexo, "edad": "", "unidad": "años"}
    descs = []
    for x in dxs:
        d = cat.from_label(x["descripcion"])[0] if x["descripcion"] else ""
        if not d:
            d = hea_banco.sugerir_lista(x["abrev"])[0]
        descs.append(hea_banco.fuente_hea(x["abrev"], d))
    ssr_dx = []        # una por cada diagnóstico del ATA (en el mismo orden); vacío si no hay equivalente en SSR
    usados = set()
    for x in dxs:
        d2 = cie11_ssr.suggest(x["abrev"], estricto=True)[:1]
        if d2 and d2[0][0] not in usados:
            usados.add(d2[0][0])
            ssr_dx.append({"abrev": x["abrev"], "descripcion": d2[0][0], "cie11": d2[0][1]})
        else:
            ssr_dx.append({"abrev": x["abrev"], "descripcion": "", "cie11": ""})
    # HEA de APS: solo los diagnósticos que no pasan a SSR (si todos pasan, se usan todos); HEA de SSR: solo los de SSR
    aps_descs = [d for d, y in zip(descs, ssr_dx) if not y["descripcion"]]
    if not any(aps_descs):
        aps_descs = descs
    # HEA de SSR: el texto del ATA cuando el banco lo conoce («PF (ACOs)» conserva el método; la lista de SSR no lo dice)
    ssr_descs = [hea_banco.fuente_hea_ssr(y["abrev"], y["descripcion"], True) for y in ssr_dx if y["descripcion"]]
    if any(aps_descs):
        hea = hea_banco.compose(persona["sexo"], persona["edad"], aps_descs, persona["unidad"])[0]
    else:
        hea = generate_hea(rec, desc)
    ssr_hea = (hea_banco.compose(persona["sexo"], persona["edad"], ssr_descs, persona["unidad"])[0]
               if ssr_descs else hea)
    vit = vitales_defecto(persona["sexo"], persona["edad"], persona["unidad"],
                          hta=any(es_hta(x["abrev"]) or es_hta(d) for x, d in zip(dxs, descs)))
    return {
        "hea": hea, "ssr_hea": ssr_hea, "hea_persona": persona, **vit,
        "ssr_mismo_punto": "Sí", "ssr_mismo_proy": "Sí", "ssr_ficha": "Larga", "ssr_recibio_aps": "Sí",
        "ssr_tipo": "Primera", "ssr_dx": ssr_dx, "ssr_va_derivado": "No", "ssr_transfronteriza": "",
        **defectos_ssr(), **defectos_obstetricos(rec),
        "ssr_servicio_brindado": "Salud", "ssr_servicio_salud": SSR_SERVICIO_SALUD, "peso": "", "examen_fisico": EXAMEN_FISICO_APS, "ssr_examen_fisico": EXAMEN_FISICO_SSR,
        "plan": PLAN_BASE, "va_derivado": "No", "n_servicios": "", "transfronteriza": "No",
        "servicio_brindado": "Salud", "servicio_salud": SERVICIOS_SALUD[0],
        "lugar": lugar_atencion(rec, st["ai_lugar"]), "punto_especifico": (rec.get("loc") or "").strip(), "fecha": (rec.get("fecha") or "")[:10], "genero": genero,
        "donante": st["ai_donante"], "proyecto": st["ai_proyecto"], "perfin": st["ai_perfin"],
        "nacionalidad": st["ai_nacionalidad"], "idioma": st["ai_idioma"],
        "nombres": nombres, "apellidos": apellidos, "telefono": telefono_internacional(rec.get("telefono")),
        "tiene_fecha_nac": "No", "edad": edad,
        **defectos_ficha(menor=es_menor_de_edad(persona["edad"], persona["unidad"]),
                         estado_civil=_ata.estado_civil_ai(rec.get("estado_civil")),
                         ocupacion=_ata.ocupacion_ai(rec.get("profesion"))), "perfil": PERFIL_FIJO,
        "ata_estado_civil": _ata.estado_civil_ai(rec.get("estado_civil")), "ata_ocupacion": _ata.ocupacion_ai(rec.get("profesion")),
        "consultas": [CONSULTA_APS], "profesional": st["ai_profesional"],
        "tipo_consulta": "Primera", "dx": dxs,
    }


def payload(data: dict) -> dict:
    """Lo que se envía al formulario. Los campos vacíos no se tocan."""
    d = {k: v for k, v in data.items() if k not in ("dx", "recordar_dx") and not k.startswith("ssr_")}
    d["permitir_esta_hecho"] = PERMITIR_ESTA_HECHO_EN_APS
    if d.get("derivado") != "Sí":                 # sin Sí no existen los campos de «Derivación (desde)»
        for k in ("derivado_procedencia", "derivado_obs", "derivado_codigo"):
            d[k] = ""
    if d.get("discapacidad") != "Sí":
        d["discapacidad_tipo"] = []
    dx = [{"abrev": x.get("abrev", ""), "descripcion": x.get("descripcion", ""), "cie11": x.get("cie11", "")}
          for x in (data.get("dx") or [])][:3]
    d["dx"] = dx
    d["n_dx"] = len(dx) or ""
    return d


def remember_dx(db, data: dict):
    """Guarda las equivalencias abreviatura → descripción/código que la persona dejó en la ventana."""
    if not data.get("recordar_dx"):
        return
    for x in data.get("dx") or []:
        if x.get("abrev") and (x.get("descripcion") or x.get("cie11")):
            save_dx_map(db, x["abrev"], x.get("descripcion", ""), x.get("cie11", ""))


# -- navegador -----------------------------------------------------------------------

def _js_source() -> str:
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent)) / "services"
    return (base / "ai_fill.js").read_text(encoding="utf-8")


def _profile_dir() -> str:
    d = Path(config.data_dir()) / "chrome_activityinfo"
    d.mkdir(parents=True, exist_ok=True)
    return str(d)


DEBUG_PORT = 9223


def _find_chrome():
    """Ruta de chrome.exe (instalación normal de Chrome) o None."""
    import os
    import shutil
    cands = [os.path.join(os.environ.get(v, ""), "Google", "Chrome", "Application", "chrome.exe")
             for v in ("PROGRAMFILES", "PROGRAMFILES(X86)", "LOCALAPPDATA")]
    for c in cands:
        if c and os.path.exists(c):
            return c
    return shutil.which("chrome") or shutil.which("google-chrome")


def _port_open(port=DEBUG_PORT):
    import socket
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=0.5):
            return True
    except OSError:
        return False


def _descartar_driver():
    """Olvida la conexión con Chrome (sin cerrar el Chrome de la persona): solo se detiene chromedriver."""
    global _driver
    d, _driver = _driver, None
    if d is not None:
        try:
            d.service.stop()
        except Exception:  # noqa: BLE001
            pass


def _sesion_sana(drv):
    """True si el driver sigue conectado a una ventana abierta. Si la persona cerró la pestaña o ventana a la que el
    driver apuntaba pero quedan otras, pasa a una de las que quedan (antes daba «no such window»)."""
    try:
        hs = drv.window_handles
    except Exception:  # noqa: BLE001
        return False
    if not hs:
        return False
    try:
        _ = drv.current_url
    except Exception:  # noqa: BLE001
        try:
            drv.switch_to.window(hs[-1])
            _ = drv.current_url
        except Exception:  # noqa: BLE001
            return False
    return True


def _ventana_muerta(exc):
    """¿El error es de una ventana o sesión de Chrome que ya no existe (se cerró)?"""
    t = str(exc).lower()
    return any(x in t for x in ("no such window", "target window already closed", "web view not found",
                                "invalid session id", "not connected to devtools", "disconnected",
                                "chrome not reachable", "session deleted", "no such execution context"))


def _abrir_chrome(chrome):
    import subprocess
    subprocess.Popen([chrome, f"--remote-debugging-port={DEBUG_PORT}",
                      f"--user-data-dir={_profile_dir()}", "--no-first-run",
                      "--no-default-browser-check", "--start-maximized", "about:blank"])


def _get_driver():
    """Chrome NORMAL (ventana de siempre, sin aviso de automatización ni modo incógnito).
    Se abre como cualquier Chrome y Selenium solo se conecta a él. Usa un perfil propio del programa
    (Chrome no deja controlar el perfil de uso diario): la primera vez se inicia sesión y queda guardada.
    Si la persona cerró la ventana (o todo el Chrome) después de un registro, se vuelve a abrir y conectar sola."""
    global _driver
    if _driver is not None:
        if _sesion_sana(_driver):
            return _driver
        _descartar_driver()          # la ventana fue cerrada
    from selenium import webdriver
    chrome = _find_chrome()
    opts = webdriver.ChromeOptions()
    if chrome:
        if not _port_open():
            _abrir_chrome(chrome)
            for _ in range(40):
                if _port_open():
                    break
                time.sleep(0.5)
        opts.add_experimental_option("debuggerAddress", f"127.0.0.1:{DEBUG_PORT}")
    else:  # sin Chrome instalado en la ruta habitual: modo anterior
        opts.add_argument(f"--user-data-dir={_profile_dir()}")
        opts.add_argument("--start-maximized")
        opts.add_argument("--no-first-run")
        opts.add_experimental_option("detach", True)
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    _driver = webdriver.Chrome(options=opts)
    if chrome and not _sesion_sana(_driver):
        # Chrome sigue en segundo plano pero sin ninguna ventana (se cerraron todas): se abre una nueva en ese mismo Chrome
        _abrir_chrome(chrome)
        for _ in range(30):
            if _sesion_sana(_driver):
                break
            time.sleep(0.5)
    return _driver


def fill_form(data: dict, wait_login_seconds=300):
    """Abre una pestaña nueva con el formulario y lo llena. Devuelve {'ficha': [...], 'aps': [...]}
    con los campos que no se pudieron llenar. No guarda nada. Si Chrome se cerró entre un registro y otro,
    se reconecta y vuelve a intentarlo una vez."""
    try:
        return _fill_form_una_vez(_get_driver(), data, wait_login_seconds)
    except Exception as exc:  # noqa: BLE001
        if not _ventana_muerta(exc):
            raise
        _descartar_driver()
        return _fill_form_una_vez(_get_driver(), data, wait_login_seconds)


def _fill_form_una_vez(drv, data, wait_login_seconds):
    if drv.current_url not in ("data:,", "about:blank", "") and "activityinfo" in drv.current_url:
        drv.switch_to.new_window("tab")  # no se toca la pestaña anterior (puede tener datos sin guardar)
    drv.get(FORM_URL)
    drv.set_script_timeout(180)
    t0 = time.time()
    while time.time() - t0 < wait_login_seconds:
        try:
            found = drv.execute_script(
                "return !!document.querySelector('label.forminput__lookup__key, .forminput__field')")
        except Exception as exc:  # noqa: BLE001
            if _ventana_muerta(exc):
                raise
            found = False             # la página está cambiando (inicio de sesión, redirecciones): se sigue esperando
        if found:
            break
        time.sleep(1)
    else:
        raise RuntimeError("No apareció el formulario. Si pide iniciar sesión, inicie sesión en la "
                           "ventana de Chrome y vuelva a pulsar «Añadir registro».")
    time.sleep(1.5)
    drv.execute_script(_js_source())
    return drv.execute_async_script(
        "const cb = arguments[arguments.length - 1];"
        "window.__mdm.run(arguments[0]).then(cb).catch(e => cb({ficha: ['Error: ' + e.message], aps: []}));",
        payload(data))


def open_form():
    """Abre el formulario en el navegador predeterminado (sin llenar)."""
    webbrowser.open(FORM_URL)

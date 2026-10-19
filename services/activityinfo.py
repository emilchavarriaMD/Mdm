"""Registro de un paciente del ATA en ActivityInfo.

Se abre Chrome (con un perfil propio del programa), se abre el formulario «newRecord» y se LLENAN
los campos. El programa NUNCA guarda: no pulsa «Guardar registro», «Guardar como borrador» ni
«Está hecho». La ficha la crea la persona a mano, después de revisar los datos.
Tampoco escribe contraseñas: si ActivityInfo pide iniciar sesión, la persona lo hace en la ventana.
"""
import sys
import time
import webbrowser
from pathlib import Path

import config

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
DISCAPACIDAD = ["Sí", "No", "Prefiere no contestar"]
DERIVADO = ["Sí", "No"]
TIPOS_CONSULTA = ["Primera", "Reconsulta", "Seguimiento", "Tamizaje de signos vitales",
                  "Nuevo motivo de consulta", "Procedimiento terapéutico no quirúrgico"]
CONSULTA_APS = "Atención Primaria de Salud"

# Valores fijos que se configuran una vez (pantalla Configuración).
SETTINGS = [
    ("ai_lugar", "Lugar de atención (al elegirlo se llenan País y Departamento)", "San Pedro Sula"),
    ("ai_nacionalidad", "País de nacionalidad", "Honduras"),
    ("ai_idioma", "Idioma", "Español"),
    ("ai_profesional", "Profesional que atiende (APS)", "Nadia Alejandra Chavarria Lopez"),
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


def build_defaults(db, rec: dict) -> dict:
    """Datos iniciales para la ventana de revisión. Solo se toma lo que está en el ATA; lo que el ATA
    no trae (estado civil, escolaridad, etc.) queda vacío para que lo elija la persona."""
    st = get_setting_values(db)
    nombres, apellidos = split_name(rec.get("nombre"))
    sexo = (rec.get("sexo") or "").upper()
    genero = {"M": "Mujer CIS", "H": "Hombre CIS"}.get(sexo, "")
    fn = (rec.get("fecha_nacimiento") or "").strip()
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
    return {
        "lugar": st["ai_lugar"], "fecha": (rec.get("fecha") or "")[:10], "genero": genero,
        "nacionalidad": st["ai_nacionalidad"], "idioma": st["ai_idioma"],
        "nombres": nombres, "apellidos": apellidos,
        "tiene_fecha_nac": "Si" if fn else "No", "fecha_nac": fn[:10], "edad": edad,
        "estado_civil": "", "escolaridad": "", "ocupacion": "", "discapacidad": "", "perfil": PERFIL_FIJO,
        "derivado": "", "consulta": CONSULTA_APS, "profesional": st["ai_profesional"],
        "tipo_consulta": "", "dx": dxs,
    }


def payload(data: dict) -> dict:
    """Lo que se envía al formulario. Los campos vacíos no se tocan."""
    d = {k: v for k, v in data.items() if k != "dx"}
    d["n_dx"] = min(len(data.get("dx") or []), 3) or ""
    return d


# -- navegador -----------------------------------------------------------------------

def _js_source() -> str:
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent)) / "services"
    return (base / "ai_fill.js").read_text(encoding="utf-8")


def _profile_dir() -> str:
    d = Path(config.data_dir()) / "chrome_activityinfo"
    d.mkdir(parents=True, exist_ok=True)
    return str(d)


def _get_driver():
    global _driver
    if _driver is not None:
        try:
            _ = _driver.window_handles
            return _driver
        except Exception:  # noqa: BLE001  (la ventana fue cerrada)
            _driver = None
    from selenium import webdriver
    opts = webdriver.ChromeOptions()
    opts.add_argument(f"--user-data-dir={_profile_dir()}")
    opts.add_argument("--start-maximized")
    opts.add_argument("--no-first-run")
    opts.add_experimental_option("detach", True)  # la ventana queda abierta aunque se cierre el programa
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    _driver = webdriver.Chrome(options=opts)
    return _driver


def fill_form(data: dict, wait_login_seconds=300):
    """Abre una pestaña nueva con el formulario y lo llena. Devuelve {'ficha': [...], 'aps': [...]}
    con los campos que no se pudieron llenar. No guarda nada."""
    drv = _get_driver()
    if drv.current_url not in ("data:,", "about:blank", "") and "activityinfo" in drv.current_url:
        drv.switch_to.new_window("tab")  # no se toca la pestaña anterior (puede tener datos sin guardar)
    drv.get(FORM_URL)
    drv.set_script_timeout(180)
    t0 = time.time()
    while time.time() - t0 < wait_login_seconds:
        found = drv.execute_script(
            "return !!document.querySelector('label.forminput__lookup__key, .forminput__field')")
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

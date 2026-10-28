"""Bitácora del llenado de ActivityInfo: una entrada por intento (paciente, qué se llenó, qué falló y por qué).
Sirve para diagnosticar problemas sin depender de capturas de pantalla. No guarda contraseñas ni textos clínicos."""
import json
from datetime import datetime
from pathlib import Path

import config

MAX_BYTES = 1_000_000


def log_path() -> Path:
    return Path(config.data_dir()) / "bitacora_llenado.log"


def resumen_fechas(report, hoy=None):
    """Líneas para el aviso final: qué fecha de consulta se escribió en la ficha, en APS y en SSR (según se leyó de vuelta en
    ActivityInfo). Avisa si alguna no es la del ATA o si es la de HOY. Lista vacía si el reporte no trae fechas."""
    f = (report or {}).get("fechas") or {}
    if not f:
        return []
    esperada = f.get("esperada") or ""
    hoy = hoy or datetime.now().strftime("%Y-%m-%d")
    partes = [(n, f[k]) for n, k in (("ficha", "ficha"), ("APS", "aps"), ("SSR", "ssr")) if k in f]
    lineas = [f"Fecha de la consulta (del ATA): {esperada or 'SIN FECHA'}"
              + (" — escrita en: " + ", ".join(f"{n} {v or '(vacía)'}" for n, v in partes) if partes else "")]
    if not esperada:
        lineas.append("⚠ El ATA no trae fecha: ActivityInfo dejó la de HOY. Corríjala a mano.")
    elif any(v != esperada for _n, v in partes):
        lineas.append("⚠ Alguna fecha no quedó como la del ATA: corríjala a mano antes de crear la ficha.")
    elif esperada == hoy:
        lineas.append("Es la fecha de HOY. Si la consulta fue otro día, corrija la fecha del encabezado de la hoja ATA.")
    return lineas


def registrar(paciente, report=None, error=None, consultas=None):
    """Agrega una línea JSON. Nunca lanza errores (la bitácora no debe estorbar al llenado)."""
    try:
        p = log_path()
        if p.exists() and p.stat().st_size > MAX_BYTES:      # al pasar de ~1 MB se conserva solo la segunda mitad
            lineas = p.read_text(encoding="utf-8").splitlines()
            p.write_text("\n".join(lineas[len(lineas) // 2:]) + "\n", encoding="utf-8")
        rep = report or {}
        entrada = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "paciente": paciente,
            "consultas": list(consultas or []), "error": str(error) if error else "",
            "no_llenados": (rep.get("ficha") or []) + (rep.get("aps") or []) + (rep.get("ssr") or []),
            "verificacion": rep.get("verif") or [], "diagnosticos": rep.get("info") or [],
            "fechas": rep.get("fechas") or {}, "version_llenado": rep.get("version"), "version_programa": config.APP_VERSION,
        }
        with p.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entrada, ensure_ascii=False) + "\n")
    except Exception:  # noqa: BLE001
        pass


def leer(max_entradas=60):
    """Últimas entradas (la más reciente primero) como lista de dicts."""
    p = log_path()
    if not p.exists():
        return []
    out = []
    for linea in p.read_text(encoding="utf-8").splitlines()[-max_entradas:]:
        try:
            out.append(json.loads(linea))
        except ValueError:
            continue
    return out[::-1]


def texto(entrada) -> str:
    e = entrada
    estado = "ERROR: " + e["error"] if e.get("error") else ("con pendientes" if e.get("no_llenados") or e.get("verificacion") else "completo")
    lineas = [f"{e.get('fecha', '')}  ·  {e.get('paciente', '')}  ·  {estado}"]
    if e.get("fechas"):
        lineas.append("   fechas: " + ", ".join(f"{k}={v or '(vacía)'}" for k, v in e["fechas"].items())
                      + f"  ·  programa {e.get('version_programa', '?')}, llenado v{e.get('version_llenado', '?')}")
    for x in e.get("no_llenados") or []:
        lineas.append("   no se llenó: " + x)
    for x in e.get("verificacion") or []:
        lineas.append("   verificación: " + x)
    return "\n".join(lineas)

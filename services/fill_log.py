"""Bitácora del llenado de ActivityInfo: una entrada por intento (paciente, qué se llenó, qué falló y por qué).
Sirve para diagnosticar problemas sin depender de capturas de pantalla. No guarda contraseñas ni textos clínicos."""
import json
from datetime import datetime
from pathlib import Path

import config

MAX_BYTES = 1_000_000


def log_path() -> Path:
    return Path(config.data_dir()) / "bitacora_llenado.log"


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
    for x in e.get("no_llenados") or []:
        lineas.append("   no se llenó: " + x)
    for x in e.get("verificacion") or []:
        lineas.append("   verificación: " + x)
    return "\n".join(lineas)

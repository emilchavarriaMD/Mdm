"""Copias de seguridad y restauración de la base de datos.

Se usa la API de respaldo de SQLite, que produce copias consistentes aunque el
programa esté abierto. La restauración valida el archivo antes de aplicarla y
crea antes una copia de seguridad de los datos actuales.
"""
import sqlite3
from datetime import datetime
from pathlib import Path

from config import backups_dir

REQUIRED_TABLES = {"patients", "aps_visits", "ssr_visits", "brigades", "settings"}
KEEP_AUTO_BACKUPS = 15


class BackupError(Exception):
    pass


def _stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def create_backup(db, destination=None, prefix="respaldo") -> Path:
    """Crea una copia de la base. Si destination es una carpeta o None, genera el nombre."""
    if destination is None:
        destination = backups_dir()
    destination = Path(destination)
    if destination.is_dir():
        destination = destination / f"{prefix}_{_stamp()}.db"
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        destination.unlink()
    target = sqlite3.connect(str(destination))
    try:
        db.conn.backup(target)
    finally:
        target.close()
    return destination


def validate_backup(path) -> dict:
    """Comprueba que el archivo sea una base válida del programa; devuelve estadísticas."""
    path = Path(path)
    if not path.is_file():
        raise BackupError("El archivo seleccionado no existe.")
    try:
        con = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    except sqlite3.Error as exc:
        raise BackupError(f"No se pudo abrir el archivo: {exc}")
    try:
        try:
            result = con.execute("PRAGMA integrity_check").fetchone()[0]
            tables = {r[0] for r in con.execute(
                "SELECT name FROM sqlite_master WHERE type='table'")}
        except sqlite3.DatabaseError as exc:
            raise BackupError(f"El archivo no es una base de datos válida: {exc}")
        if result != "ok":
            raise BackupError("La copia de seguridad está dañada (falló la verificación de integridad).")
        missing = REQUIRED_TABLES - tables
        if missing:
            raise BackupError("El archivo no corresponde a este programa "
                              f"(faltan tablas: {', '.join(sorted(missing))}).")
        return {
            "pacientes": con.execute("SELECT COUNT(*) FROM patients").fetchone()[0],
            "aps": con.execute("SELECT COUNT(*) FROM aps_visits").fetchone()[0],
            "ssr": con.execute("SELECT COUNT(*) FROM ssr_visits").fetchone()[0],
            "ata": (con.execute("SELECT COUNT(*) FROM ata_rows").fetchone()[0]
                    if con.execute("SELECT 1 FROM sqlite_master WHERE name='ata_rows'").fetchone() else 0),
        }
    finally:
        con.close()


def restore_backup(db, source) -> dict:
    """Restaura la base desde una copia. Devuelve las estadísticas de lo restaurado.

    Antes de reemplazar los datos se guarda una copia 'previa_restauracion'.
    """
    stats = validate_backup(source)
    create_backup(db, prefix="previa_restauracion")
    src = sqlite3.connect(str(source))
    try:
        src.backup(db.conn)
    finally:
        src.close()
    db.conn.execute("PRAGMA foreign_keys = ON")
    db.init_schema()  # por si la copia es de una versión anterior
    db.audit("sistema", None, "restauración", f"Restaurada desde {Path(source).name}")
    return stats


def list_backups():
    folder = backups_dir()
    files = sorted(folder.glob("*.db"), key=lambda p: p.stat().st_mtime, reverse=True)
    return files


def _rotar(folder, prefix, keep):
    """Conserva solo las `keep` copias más recientes con ese prefijo en la carpeta."""
    files = sorted(Path(folder).glob(f"{prefix}_*.db"), key=lambda p: p.stat().st_mtime, reverse=True)
    for old in files[keep:]:
        try:
            old.unlink()
        except OSError:
            pass


def extra_dir(db):
    """Segunda ubicación de respaldo elegida por la persona (OneDrive, USB…), o None."""
    d = (db.get_setting("respaldo_extra_dir", "") or "").strip()
    return Path(d) if d else None


def auto_backup(db, prefix="auto", keep=KEEP_AUTO_BACKUPS) -> Path:
    """Copia automática (al cerrar o cada cierto tiempo). Conserva solo las más recientes y, si hay una
    segunda ubicación configurada, deja ahí otra copia (un fallo en esa ubicación no impide la copia local)."""
    path = create_backup(db, prefix=prefix)
    _rotar(backups_dir(), prefix, keep)
    extra = extra_dir(db)
    if extra is not None:
        try:
            extra.mkdir(parents=True, exist_ok=True)
            create_backup(db, extra, prefix=prefix)
            _rotar(extra, prefix, keep)
            db.set_setting("respaldo_extra_error", "")
        except Exception as exc:  # noqa: BLE001  (USB desconectado, carpeta sin permiso…)
            db.set_setting("respaldo_extra_error", str(exc))
    db.set_setting("respaldo_ultimo", _stamp())
    return path

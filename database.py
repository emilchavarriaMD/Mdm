"""Base de datos SQLite: conexión, esquema relacional, catálogos, ajustes y auditoría.

Diseño:
  patients (1) ──< aps_visits ──< aps_exam / aps_dx / aps_meds
           └────< ssr_visits ──< ssr_exam / ssr_dx / ssr_meds / ssr_tests / ssr_interventions
  brigades (1) ──< patients, aps_visits, ssr_visits
  audit_log: historial de modificaciones relevantes.

La Ficha Integral (patients) existe una sola vez por paciente; las atenciones
APS y SSR se vinculan con patient_id y nunca duplican los datos generales.
"""
import sqlite3
from contextlib import contextmanager
from datetime import datetime

from config import SCHEMA_VERSION

DEPARTAMENTOS_HN = [
    "Atlántida", "Choluteca", "Colón", "Comayagua", "Copán", "Cortés", "El Paraíso",
    "Francisco Morazán", "Gracias a Dios", "Intibucá", "Islas de la Bahía", "La Paz",
    "Lempira", "Ocotepeque", "Olancho", "Santa Bárbara", "Valle", "Yoro",
]

DEFAULT_CATALOGS = {
    "estado_migratorio": [
        "No migrante (nacional o residente)", "Migrante en tránsito", "Migrante retornado",
        "Migrante con residencia", "Solicitante de refugio", "Desplazado interno",
        "No especificado",
    ],
    "departamento": DEPARTAMENTOS_HN,
    "categoria_ssr": [
        "Planificación familiar", "Inicio de método anticonceptivo",
        "Continuación de método anticonceptivo", "Cambio de método anticonceptivo",
        "Anticoncepción de emergencia", "Infección de transmisión sexual (ITS)",
        "Infección urinaria", "Alteración menstrual", "Flujo vaginal anormal",
        "Prurito genital", "Dolor pélvico", "Otro problema ginecológico o de SSR",
    ],
    "via_administracion": [
        "Oral", "Intramuscular", "Intravenosa", "Subcutánea", "Tópica", "Oftálmica",
        "Ótica", "Nasal", "Vaginal", "Rectal", "Inhalada", "Sublingual", "Otra",
    ],
    "unidad_cantidad": [
        "tabletas", "cápsulas", "ml", "frascos", "ampollas", "sobres", "dosis",
        "unidades", "tubos", "óvulos", "otra",
    ],
    "personal": [],
}

DEFAULT_SETTINGS = {
    "encabezado_institucion": "Brigada Médica",
    "encabezado_subtitulo": "Registro clínico digital",
    "brigada_actual": "",
    "operador": "Operador",
    "respaldo_al_salir": "1",
    "ultimo_personal": "",
}

# ---------------------------------------------------------------------------
# Esquema
# ---------------------------------------------------------------------------

_VITALS = """
    pas REAL, pad REAL, fc REAL, fr REAL, temperatura REAL, peso REAL, vitales_nota TEXT,
"""

_BASE_SCHEMA = """
CREATE TABLE IF NOT EXISTS settings (
    key   TEXT PRIMARY KEY,
    value TEXT
);

CREATE TABLE IF NOT EXISTS catalogs (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    value    TEXT NOT NULL,
    sort     INTEGER NOT NULL DEFAULT 0,
    UNIQUE (category, value)
);

CREATE TABLE IF NOT EXISTS brigades (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo       TEXT NOT NULL UNIQUE,
    nombre       TEXT NOT NULL,
    fecha        TEXT NOT NULL,
    departamento TEXT,
    municipio    TEXT,
    localidad    TEXT,
    lugar        TEXT,
    personal     TEXT,
    observaciones TEXT,
    created_at   TEXT NOT NULL,
    updated_at   TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS patients (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo           TEXT NOT NULL UNIQUE,
    historia_clinica TEXT,
    nombres          TEXT NOT NULL,
    apellidos        TEXT NOT NULL,
    nombre_norm      TEXT NOT NULL,
    fecha_nacimiento TEXT,
    edad_valor       INTEGER,
    edad_unidad      TEXT DEFAULT 'años',
    sexo             TEXT,
    telefono         TEXT,
    telefono_norm    TEXT,
    estado_migratorio TEXT,
    departamento     TEXT,
    municipio        TEXT,
    localidad        TEXT,
    fecha_creacion   TEXT NOT NULL,
    brigade_id       INTEGER REFERENCES brigades(id) ON DELETE SET NULL,
    observaciones    TEXT,
    created_at       TEXT NOT NULL,
    updated_at       TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_patients_nombre ON patients(nombre_norm);
CREATE INDEX IF NOT EXISTS idx_patients_hc ON patients(historia_clinica);
CREATE INDEX IF NOT EXISTS idx_patients_tel ON patients(telefono_norm);
CREATE INDEX IF NOT EXISTS idx_patients_brigade ON patients(brigade_id);

CREATE TABLE IF NOT EXISTS audit_log (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    ts         TEXT NOT NULL,
    usuario    TEXT,
    entidad    TEXT NOT NULL,
    entidad_id INTEGER,
    patient_id INTEGER,
    accion     TEXT NOT NULL,
    detalle    TEXT
);
CREATE INDEX IF NOT EXISTS idx_audit_entidad ON audit_log(entidad, entidad_id);
CREATE INDEX IF NOT EXISTS idx_audit_patient ON audit_log(patient_id);
"""

_APS_SCHEMA = f"""
CREATE TABLE IF NOT EXISTS aps_visits (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id       INTEGER NOT NULL REFERENCES patients(id) ON DELETE RESTRICT,
    fecha_atencion   TEXT NOT NULL,
    personal         TEXT,
    brigade_id       INTEGER REFERENCES brigades(id) ON DELETE SET NULL,
    lugar            TEXT,
    historia_clinica TEXT,
    mismo_dia_ficha  TEXT NOT NULL DEFAULT 'No' CHECK (mismo_dia_ficha IN ('Sí','No')),
    mismo_dia_manual INTEGER NOT NULL DEFAULT 0,
    observaciones    TEXT,
    hea_motivo TEXT, hea_inicio TEXT, hea_sintomas TEXT, hea_evolucion TEXT,
    hea_asociados TEXT, hea_factores TEXT, hea_antecedentes TEXT, hea_negativos TEXT,
    hea_otros TEXT, hea_texto TEXT,
    hea_origen   TEXT NOT NULL DEFAULT 'manual',
    hea_revisada INTEGER NOT NULL DEFAULT 0,
    {_VITALS}
    consejeria_alarma TEXT,
    consejeria_estado TEXT NOT NULL DEFAULT 'Pendiente',
    recomendaciones TEXT, medidas_no_farm TEXT, seguimiento TEXT,
    fecha_control TEXT, referencia TEXT,
    estado       TEXT NOT NULL DEFAULT 'borrador' CHECK (estado IN ('borrador','finalizada')),
    created_at   TEXT NOT NULL,
    updated_at   TEXT NOT NULL,
    finalizada_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_aps_patient ON aps_visits(patient_id);
CREATE INDEX IF NOT EXISTS idx_aps_fecha ON aps_visits(fecha_atencion);
CREATE INDEX IF NOT EXISTS idx_aps_brigade ON aps_visits(brigade_id);
"""

_SSR_SCHEMA = f"""
CREATE TABLE IF NOT EXISTS ssr_visits (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id       INTEGER NOT NULL REFERENCES patients(id) ON DELETE RESTRICT,
    fecha_atencion   TEXT NOT NULL,
    personal         TEXT,
    brigade_id       INTEGER REFERENCES brigades(id) ON DELETE SET NULL,
    lugar            TEXT,
    motivo           TEXT,
    categoria        TEXT,
    mismo_dia_aps    TEXT NOT NULL DEFAULT 'No se registró atención APS'
                     CHECK (mismo_dia_aps IN ('Sí','No','No se registró atención APS')),
    mismo_dia_manual INTEGER NOT NULL DEFAULT 0,
    observaciones    TEXT,
    hea_inicio TEXT, hea_urinarios TEXT, hea_flujo TEXT, hea_olor_prurito TEXT,
    hea_dolor TEXT, fum TEXT, hea_ciclo TEXT, hea_antec_go TEXT,
    hea_anticonceptivo_actual TEXT, hea_fecha_ultima_dosis TEXT,
    hea_riesgo_embarazo TEXT, hea_antec_its TEXT, hea_otros TEXT, hea_texto TEXT,
    hea_origen   TEXT NOT NULL DEFAULT 'manual',
    hea_revisada INTEGER NOT NULL DEFAULT 0,
    {_VITALS}
    metodo_entregado TEXT, metodo_presentacion TEXT, metodo_cantidad REAL,
    metodo_unidad TEXT, fecha_administracion TEXT, fecha_proxima_dosis TEXT,
    signos_alarma TEXT, recomendaciones TEXT, seguimiento TEXT,
    fecha_control TEXT, referencia TEXT,
    estado       TEXT NOT NULL DEFAULT 'borrador' CHECK (estado IN ('borrador','finalizada')),
    created_at   TEXT NOT NULL,
    updated_at   TEXT NOT NULL,
    finalizada_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_ssr_patient ON ssr_visits(patient_id);
CREATE INDEX IF NOT EXISTS idx_ssr_fecha ON ssr_visits(fecha_atencion);
CREATE INDEX IF NOT EXISTS idx_ssr_brigade ON ssr_visits(brigade_id);
"""


def _child_tables(prefix: str) -> str:
    return f"""
CREATE TABLE IF NOT EXISTS {prefix}_exam (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    visit_id  INTEGER NOT NULL REFERENCES {prefix}_visits(id) ON DELETE CASCADE,
    region    TEXT NOT NULL,
    estado    TEXT NOT NULL,
    hallazgos TEXT,
    UNIQUE (visit_id, region)
);
CREATE TABLE IF NOT EXISTS {prefix}_dx (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    visit_id    INTEGER NOT NULL REFERENCES {prefix}_visits(id) ON DELETE CASCADE,
    tipo        TEXT NOT NULL CHECK (tipo IN ('principal','secundario')),
    descripcion TEXT NOT NULL,
    descripcion_norm TEXT NOT NULL,
    cie11       TEXT,
    cie11_verificado INTEGER NOT NULL DEFAULT 0,
    observaciones TEXT,
    orden       INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_{prefix}_dx_visit ON {prefix}_dx(visit_id);
CREATE INDEX IF NOT EXISTS idx_{prefix}_dx_norm ON {prefix}_dx(descripcion_norm);
CREATE TABLE IF NOT EXISTS {prefix}_meds (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    visit_id     INTEGER NOT NULL REFERENCES {prefix}_visits(id) ON DELETE CASCADE,
    generico     TEXT NOT NULL,
    presentacion TEXT,
    dosis        TEXT,
    via          TEXT,
    frecuencia   TEXT,
    horario      TEXT,
    duracion     TEXT,
    cant_prescrita REAL,
    cant_entregada REAL,
    unidad       TEXT,
    indicaciones TEXT,
    orden        INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_{prefix}_meds_visit ON {prefix}_meds(visit_id);
"""


_SSR_EXTRA = """
CREATE TABLE IF NOT EXISTS ssr_tests (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    visit_id  INTEGER NOT NULL REFERENCES ssr_visits(id) ON DELETE CASCADE,
    prueba    TEXT NOT NULL,
    estado    TEXT NOT NULL DEFAULT 'Realizada' CHECK (estado IN ('Realizada','No realizada','Pendiente')),
    resultado TEXT,
    motivo    TEXT,
    orden     INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS ssr_interventions (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    visit_id  INTEGER NOT NULL REFERENCES ssr_visits(id) ON DELETE CASCADE,
    tipo      TEXT NOT NULL,
    estado    TEXT NOT NULL DEFAULT 'Pendiente' CHECK (estado IN ('Realizada','No realizada','Pendiente')),
    nota      TEXT,
    UNIQUE (visit_id, tipo)
);
"""

_ATA_SCHEMA = """
CREATE TABLE IF NOT EXISTS ata_sheets (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha         TEXT,
    establecimiento TEXT,
    profesional   TEXT,
    codigo        TEXT,
    tipo_establecimiento TEXT,
    departamento  TEXT,
    municipio     TEXT,
    brigade_id    INTEGER REFERENCES brigades(id) ON DELETE SET NULL,
    imagen        TEXT,
    created_at    TEXT NOT NULL,
    updated_at    TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS ata_rows (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    sheet_id  INTEGER NOT NULL REFERENCES ata_sheets(id) ON DELETE CASCADE,
    orden     INTEGER NOT NULL DEFAULT 0,
    numero TEXT, hc TEXT, nombre TEXT, identidad TEXT, sexo TEXT,
    fecha_nacimiento TEXT, edad_anios TEXT, edad_meses TEXT, edad_dias TEXT,
    dep TEXT, mun TEXT, loc TEXT,
    dx1 TEXT, cie1 TEXT, dx2 TEXT, cie2 TEXT, dx3 TEXT, cie3 TEXT,
    ref_enviada TEXT, ref_recibida TEXT
);
CREATE INDEX IF NOT EXISTS idx_ata_rows_sheet ON ata_rows(sheet_id);
CREATE TABLE IF NOT EXISTS dx_map (
    abrev       TEXT PRIMARY KEY,
    descripcion TEXT NOT NULL DEFAULT '',
    cie11       TEXT NOT NULL DEFAULT ''
);
"""


def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class Database:
    """Envoltorio fino sobre sqlite3 con transacciones anidables."""

    def __init__(self, path):
        self.path = str(path)
        self.conn = sqlite3.connect(self.path, timeout=15)
        self.conn.row_factory = sqlite3.Row
        self.conn.isolation_level = None  # autocommit; las transacciones se manejan a mano
        self.conn.execute("PRAGMA foreign_keys = ON")
        self._depth = 0
        self.init_schema()

    # -- ciclo de vida --------------------------------------------------
    def close(self):
        try:
            self.conn.close()
        except sqlite3.Error:
            pass

    def init_schema(self):
        # executescript hace COMMIT implícito, por eso se usa fuera de transacciones.
        for script in (_BASE_SCHEMA, _APS_SCHEMA, _SSR_SCHEMA,
                       _child_tables("aps"), _child_tables("ssr"), _SSR_EXTRA, _ATA_SCHEMA):
            self.conn.executescript(script)
        # Migración: número de identidad en la Ficha Integral (bases creadas antes de esta versión).
        cols = [r["name"] for r in self.conn.execute("PRAGMA table_info(patients)").fetchall()]
        if "identidad" not in cols:
            self.conn.execute("ALTER TABLE patients ADD COLUMN identidad TEXT")
        acols = [r["name"] for r in self.conn.execute("PRAGMA table_info(ata_rows)").fetchall()]
        if "ai_estado" not in acols:
            self.conn.execute("ALTER TABLE ata_rows ADD COLUMN ai_estado TEXT NOT NULL DEFAULT 'Pendiente'")
            self.conn.execute("ALTER TABLE ata_rows ADD COLUMN ai_fecha TEXT")
        for col in ("telefono", "obst"):   # plantilla ATA-2023: teléfono y gestas/partos/cesáreas/abortos/HV/HM
            if col not in acols:
                self.conn.execute(f"ALTER TABLE ata_rows ADD COLUMN {col} TEXT")
        if "ai_datos" not in acols:        # lo que se llenó en ActivityInfo (para volver a ver el registro)
            self.conn.execute("ALTER TABLE ata_rows ADD COLUMN ai_datos TEXT")
        if "borrado_en" not in acols:      # papelera: los pacientes borrados se pueden recuperar
            self.conn.execute("ALTER TABLE ata_rows ADD COLUMN borrado_en TEXT")
        self.conn.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")
        with self.transaction():
            for key, value in DEFAULT_SETTINGS.items():
                self.conn.execute(
                    "INSERT OR IGNORE INTO settings(key, value) VALUES (?, ?)", (key, value))
            for category, values in DEFAULT_CATALOGS.items():
                for i, value in enumerate(values):
                    self.conn.execute(
                        "INSERT OR IGNORE INTO catalogs(category, value, sort) VALUES (?,?,?)",
                        (category, value, i))

    # -- consultas ------------------------------------------------------
    def execute(self, sql, params=()):
        return self.conn.execute(sql, params)

    def query(self, sql, params=()):
        return [dict(r) for r in self.conn.execute(sql, params).fetchall()]

    def one(self, sql, params=()):
        row = self.conn.execute(sql, params).fetchone()
        return dict(row) if row else None

    def scalar(self, sql, params=()):
        row = self.conn.execute(sql, params).fetchone()
        return row[0] if row else None

    @contextmanager
    def transaction(self):
        outermost = self._depth == 0
        if outermost:
            self.conn.execute("BEGIN")
        self._depth += 1
        try:
            yield
        except BaseException:
            self._depth -= 1
            if outermost:
                self.conn.execute("ROLLBACK")
            raise
        else:
            self._depth -= 1
            if outermost:
                self.conn.execute("COMMIT")

    # -- ajustes --------------------------------------------------------
    def get_setting(self, key, default=""):
        row = self.conn.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
        return row[0] if row and row[0] is not None else default

    def set_setting(self, key, value):
        self.conn.execute(
            "INSERT INTO settings(key, value) VALUES (?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value=excluded.value", (key, str(value)))

    # -- catálogos configurables ---------------------------------------
    def catalog(self, category):
        return [r[0] for r in self.conn.execute(
            "SELECT value FROM catalogs WHERE category=? ORDER BY sort, value", (category,))]

    def add_catalog(self, category, value):
        value = (value or "").strip()
        if not value:
            return False
        nxt = self.scalar("SELECT COALESCE(MAX(sort), -1) + 1 FROM catalogs WHERE category=?",
                          (category,))
        cur = self.conn.execute(
            "INSERT OR IGNORE INTO catalogs(category, value, sort) VALUES (?,?,?)",
            (category, value, nxt))
        return cur.rowcount > 0

    def remove_catalog(self, category, value):
        self.conn.execute("DELETE FROM catalogs WHERE category=? AND value=?", (category, value))

    def distinct_values(self, table, column):
        allowed = {("patients", "municipio"), ("patients", "localidad"),
                   ("aps_visits", "lugar"), ("ssr_visits", "lugar"),
                   ("brigades", "municipio"), ("brigades", "localidad"), ("brigades", "lugar")}
        if (table, column) not in allowed:
            raise ValueError("columna no permitida")
        return [r[0] for r in self.conn.execute(
            f"SELECT DISTINCT {column} FROM {table} "
            f"WHERE {column} IS NOT NULL AND TRIM({column}) <> '' ORDER BY {column}")]

    # -- auditoría ------------------------------------------------------
    def audit(self, entidad, entidad_id, accion, detalle="", patient_id=None):
        self.conn.execute(
            "INSERT INTO audit_log(ts, usuario, entidad, entidad_id, patient_id, accion, detalle) "
            "VALUES (?,?,?,?,?,?,?)",
            (now_iso(), self.get_setting("operador", "Operador"), entidad, entidad_id,
             patient_id, accion, detalle))

"""Tema visual (ttk 'clam' personalizado): colores, fuentes y estilos."""
import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk

CLARO = dict(
    PRIMARY="#0F6E7C", PRIMARY_DARK="#0A525D", PRIMARY_LIGHT="#E3F1F4", PRIMARY_LIGHT2="#D5E8EC",
    BG="#F3F6F7", CARD="#FFFFFF", FIELD="#FFFFFF", FIELD_DIS="#EDF0F1", TEXT="#1F2A30", MUTED="#5F6B70",
    BORDER="#C5D1D6", DANGER="#B3261E", DANGER_BG="#F8E3E1", DANGER_ACT="#F1CBC7", BAD_BG="#FDECEA",
    WARN="#9A5B00", WARN_BG="#FFF3D6", OK="#1B7F4B", OK_BG="#DDF3E6",
    SIDEBAR="#0B3C45", SIDEBAR_HOVER="#12525D", SUGGEST_BG="#FFFBEA",
    BTN="#E6ECEE", BTN_ACT="#D5DFE2", BTN_DIS="#EEF1F2", BTN_DIS_FG="#9AA5A9", TROUGH="#E4EAEC",
    ODD="#F4F8F9", ACCENT_HOVER="#0A525D", ACCENT_DIS="#9DBFC5", TAB_BG="#DCE5E8", HEAD_ACT="#CFE6EA",
    ENTRY_DIS_FG="#7C878B", DASH="#9DB7BD", HINT_ICON="#7FA3AB", SIDEBAR_SUB="#9CC4CB")
OSCURO = dict(   # gris cálido y acento terracota, como el modo oscuro de Claude Code
    PRIMARY="#C2603F", PRIMARY_DARK="#E8946F", PRIMARY_LIGHT="#33302D", PRIMARY_LIGHT2="#3D3935",
    BG="#1F1E1C", CARD="#292825", FIELD="#32302D", FIELD_DIS="#2A2926", TEXT="#ECE9E2", MUTED="#A29E94",
    BORDER="#45423D", DANGER="#F08A7E", DANGER_BG="#4A2B27", DANGER_ACT="#5E3631", BAD_BG="#4A2B27",
    WARN="#E8B25A", WARN_BG="#3B3220", OK="#7FD39B", OK_BG="#22392B",
    SIDEBAR="#161513", SIDEBAR_HOVER="#25231F", SUGGEST_BG="#38321F",
    BTN="#3A3733", BTN_ACT="#4A4640", BTN_DIS="#2C2A27", BTN_DIS_FG="#77736B", TROUGH="#2B2927",
    ODD="#2D2B28", ACCENT_HOVER="#A94E30", ACCENT_DIS="#5A3A2E", TAB_BG="#2F2D2A", HEAD_ACT="#4A3A31",
    ENTRY_DIS_FG="#86827A", DASH="#5C5851", HINT_ICON="#8B8680", SIDEBAR_SUB="#8B8680")
globals().update(CLARO)                  # valores por defecto (los de setup() los reemplazan según la preferencia)

LETRAS = {"Normal": 11, "Grande": 13, "Muy grande": 15}
PREFS_FILE = "ui_prefs.json"

FAMILY = "TkDefaultFont"
FONT = (FAMILY, 11)
FONT_B = (FAMILY, 11, "bold")
FONT_H1 = (FAMILY, 20, "bold")
FONT_H2 = (FAMILY, 14, "bold")
FONT_SMALL = (FAMILY, 9)
FONT_TEXT = (FAMILY, 11)
FONT_BIG = (FAMILY, 30, "bold")


def cargar_prefs():
    """Preferencias de apariencia (tema y tamaño de letra); archivo ui_prefs.json en la carpeta de datos."""
    import json
    base = {"tema": "Claro", "letra": "Normal"}
    try:
        import config
        d = json.loads((config.data_dir() / PREFS_FILE).read_text(encoding="utf-8"))
        base.update({k: d[k] for k in base if d.get(k)})
    except Exception:  # noqa: BLE001
        pass
    return base


def guardar_prefs(tema, letra):
    import json
    import config
    (config.data_dir() / PREFS_FILE).write_text(json.dumps({"tema": tema, "letra": letra}), encoding="utf-8")


def _pick_family(root):
    available = {f.lower(): f for f in tkfont.families(root)}
    for name in ("Segoe UI", "Helvetica Neue", "Noto Sans", "DejaVu Sans", "Liberation Sans",
                 "Arial", "Helvetica"):
        if name.lower() in available:
            return available[name.lower()]
    return "TkDefaultFont"


def setup(root: tk.Tk):
    global FAMILY, FONT, FONT_B, FONT_H1, FONT_H2, FONT_SMALL, FONT_TEXT, FONT_BIG
    prefs = cargar_prefs()
    globals().update(OSCURO if prefs["tema"] == "Oscuro" else CLARO)
    base = LETRAS.get(prefs["letra"], 11)
    FAMILY = _pick_family(root)
    FONT = (FAMILY, base)
    FONT_B = (FAMILY, base, "bold")
    FONT_H1 = (FAMILY, base + 9, "bold")
    FONT_H2 = (FAMILY, base + 3, "bold")
    FONT_SMALL = (FAMILY, base - 2)
    FONT_TEXT = (FAMILY, base)
    FONT_BIG = (FAMILY, base + 19, "bold")

    for name in ("TkDefaultFont", "TkTextFont", "TkMenuFont", "TkHeadingFont", "TkCaptionFont",
                 "TkTooltipFont"):
        try:
            tkfont.nametofont(name).configure(family=FAMILY, size=base)
        except tk.TclError:
            pass
    root.configure(bg=BG)
    root.option_add("*TCombobox*Listbox.font", FONT)
    root.option_add("*TCombobox*Listbox.selectBackground", PRIMARY)
    root.option_add("*TCombobox*Listbox.background", FIELD)
    root.option_add("*TCombobox*Listbox.foreground", TEXT)
    root.option_add("*Text.background", FIELD)
    root.option_add("*Text.foreground", TEXT)
    root.option_add("*Text.insertBackground", TEXT)
    root.option_add("*Text.selectBackground", PRIMARY)
    root.option_add("*Text.selectForeground", "white")
    root.option_add("*TCombobox*Listbox.selectForeground", "white")

    s = ttk.Style(root)
    s.theme_use("clam")
    s.configure(".", background=BG, foreground=TEXT, font=FONT, bordercolor=BORDER,
                lightcolor=BG, darkcolor=BG, troughcolor=TROUGH, focuscolor=PRIMARY)

    s.configure("TFrame", background=BG)
    s.configure("Card.TFrame", background=CARD, relief="solid", borderwidth=1, bordercolor=BORDER,
                lightcolor=CARD, darkcolor=CARD)
    s.configure("Flat.TFrame", background=CARD)
    s.configure("Sidebar.TFrame", background=SIDEBAR)
    s.configure("Strip.TFrame", background=PRIMARY_LIGHT)

    s.configure("TLabel", background=BG, foreground=TEXT, font=FONT)
    s.configure("Card.TLabel", background=CARD)
    s.configure("Muted.TLabel", foreground=MUTED)
    s.configure("CardMuted.TLabel", background=CARD, foreground=MUTED)
    s.configure("Strip.TLabel", background=PRIMARY_LIGHT)
    s.configure("StripB.TLabel", background=PRIMARY_LIGHT, font=FONT_B)
    s.configure("StripOk.TLabel", background=PRIMARY_LIGHT, foreground=OK, font=FONT_B)
    s.configure("StripWarn.TLabel", background=PRIMARY_LIGHT, foreground=WARN, font=FONT_B)
    s.configure("NavItem.TLabel", background=CARD, foreground=TEXT, font=FONT)
    s.configure("H1.TLabel", font=FONT_H1, foreground=PRIMARY_DARK)
    s.configure("H2.TLabel", font=FONT_H2, foreground=PRIMARY_DARK)
    s.configure("Field.TLabel", font=(FAMILY, 10, "bold"), foreground=MUTED)
    s.configure("CardField.TLabel", font=(FAMILY, 10, "bold"), foreground=MUTED, background=CARD)
    s.configure("StatNum.TLabel", font=FONT_BIG, foreground=PRIMARY, background=CARD)
    s.configure("StatCap.TLabel", font=FONT_B, foreground=MUTED, background=CARD)
    s.configure("StatSub.TLabel", font=FONT_SMALL, foreground=MUTED, background=CARD)
    s.configure("SidebarTitle.TLabel", background=SIDEBAR, foreground="white", font=(FAMILY, 13, "bold"))
    s.configure("SidebarSub.TLabel", background=SIDEBAR, foreground=SIDEBAR_SUB, font=FONT_SMALL)
    s.configure("Draft.TLabel", background=WARN_BG, foreground=WARN, font=FONT_B, padding=(10, 4))
    s.configure("Final.TLabel", background=OK_BG, foreground=OK, font=FONT_B, padding=(10, 4))
    s.configure("Dirty.TLabel", foreground=DANGER, font=FONT_B)
    s.configure("Saved.TLabel", foreground=OK, font=FONT_B)
    s.configure("Warn.TLabel", foreground=WARN, font=FONT_B)
    s.configure("Error.TLabel", foreground=DANGER, font=FONT_B)

    s.configure("TButton", padding=(14, 7), font=FONT, background=BTN, foreground=TEXT,
                bordercolor=BORDER, relief="flat", focusthickness=2, width=0)
    s.map("TButton", background=[("disabled", BTN_DIS), ("active", BTN_ACT)],
          foreground=[("disabled", BTN_DIS_FG)])
    s.configure("Accent.TButton", background=PRIMARY, foreground="white", font=FONT_B,
                bordercolor=PRIMARY_DARK)
    s.map("Accent.TButton", background=[("disabled", ACCENT_DIS), ("active", ACCENT_HOVER)],
          foreground=[("disabled", "#F0F5F6")])
    s.configure("Danger.TButton", background=DANGER_BG, foreground=DANGER, font=FONT_B)
    s.map("Danger.TButton", background=[("disabled", BTN_DIS), ("active", DANGER_ACT)])
    s.configure("Small.TButton", padding=(8, 3), font=(FAMILY, 10))
    s.configure("Nav.TButton", background=SIDEBAR, foreground="white", anchor="w", padding=(18, 11),
                font=FONT, relief="flat", borderwidth=0)
    s.map("Nav.TButton", background=[("active", SIDEBAR_HOVER)])
    s.configure("NavActive.TButton", background=PRIMARY, foreground="white", anchor="w",
                padding=(18, 11), font=FONT_B, relief="flat", borderwidth=0)
    s.map("NavActive.TButton", background=[("active", PRIMARY)])
    s.configure("Strip.TButton", background=CARD, padding=(10, 5), font=(FAMILY, 10, "bold"))
    s.map("Strip.TButton", background=[("active", PRIMARY_LIGHT2)])

    s.configure("TEntry", fieldbackground=FIELD, foreground=TEXT, padding=6, bordercolor=BORDER, lightcolor=FIELD,
                darkcolor=FIELD)
    s.map("TEntry", bordercolor=[("focus", PRIMARY)], fieldbackground=[("disabled", FIELD_DIS),
                                                                       ("readonly", FIELD_DIS)])
    s.configure("Bad.TEntry", fieldbackground=BAD_BG, foreground=DANGER, padding=6,
                bordercolor=DANGER, lightcolor=BAD_BG, darkcolor=BAD_BG)
    s.configure("Hint.TLabel", foreground=MUTED, font=FONT_SMALL)
    s.configure("Note.TLabel", foreground=WARN, background=WARN_BG, font=FONT, padding=(10, 6))
    s.configure("TCombobox", fieldbackground=FIELD, foreground=TEXT, padding=6, bordercolor=BORDER,
                lightcolor=FIELD, darkcolor=FIELD, arrowsize=16, background=BTN)
    s.configure("Bad.TCombobox", fieldbackground=BAD_BG, foreground=DANGER, padding=6, bordercolor=DANGER,
                lightcolor=BAD_BG, darkcolor=BAD_BG, arrowsize=16, background=BTN)
    s.map("Bad.TCombobox", fieldbackground=[("readonly", BAD_BG)])
    s.map("TCombobox", bordercolor=[("focus", PRIMARY)],
          fieldbackground=[("disabled", FIELD_DIS), ("readonly", FIELD)],
          foreground=[("disabled", ENTRY_DIS_FG)])
    for nombre, fondo in (("TCheckbutton", BG), ("Card.TCheckbutton", CARD), ("TRadiobutton", BG),
                          ("Card.TRadiobutton", CARD)):
        s.configure(nombre, background=fondo, foreground=TEXT, font=FONT, indicatorbackground=FIELD,
                    indicatorforeground="white", bordercolor=BORDER, lightcolor=FIELD, darkcolor=FIELD,
                    focuscolor=fondo)
        s.map(nombre, indicatorbackground=[("selected", PRIMARY), ("pressed", BTN_ACT), ("!selected", FIELD)],
              background=[("active", fondo)], foreground=[("disabled", BTN_DIS_FG)])
    s.configure("TScrollbar", background=BTN, troughcolor=TROUGH, bordercolor=TROUGH, arrowcolor=MUTED,
                lightcolor=BTN, darkcolor=BTN, gripcount=0, relief="flat")
    s.map("TScrollbar", background=[("pressed", PRIMARY), ("active", BTN_ACT)],
          arrowcolor=[("pressed", TEXT), ("active", TEXT)])

    s.configure("TNotebook", background=BG, borderwidth=0, tabmargins=(0, 4, 0, 0))
    s.configure("TNotebook.Tab", padding=(14, 8), font=FONT_B, background=TAB_BG, foreground=MUTED,
                bordercolor=BORDER)
    s.map("TNotebook.Tab", background=[("selected", CARD)], foreground=[("selected", PRIMARY_DARK)],
          expand=[("selected", (0, 2, 0, 0))])

    s.configure("Treeview", rowheight=base * 3 - 3, font=FONT, background=FIELD, foreground=TEXT, fieldbackground=FIELD,
                bordercolor=BORDER)
    s.configure("Treeview.Heading", font=FONT_B, background=PRIMARY_LIGHT, foreground=PRIMARY_DARK,
                padding=(8, 7), relief="flat")
    s.map("Treeview.Heading", background=[("active", HEAD_ACT)])
    s.map("Treeview", background=[("selected", PRIMARY)], foreground=[("selected", "white")])

    s.configure("TLabelframe", background=BG, bordercolor=BORDER, relief="solid", borderwidth=1,
                lightcolor=BG, darkcolor=BG)
    s.configure("TLabelframe.Label", background=BG, foreground=PRIMARY_DARK, font=FONT_B)
    s.configure("Card.TLabelframe", background=CARD, lightcolor=CARD, darkcolor=CARD)
    s.configure("Card.TLabelframe.Label", background=CARD, foreground=PRIMARY_DARK, font=FONT_B)
    s.configure("TSeparator", background=BORDER)
    s.configure("TPanedwindow", background=BG)
    s.configure("Horizontal.TProgressbar", background=PRIMARY)
    return s


def barra_titulo_oscura(root):
    """En Windows 10/11 pone la barra de título negra cuando el tema es oscuro (si falla, queda como estaba)."""
    if cargar_prefs()["tema"] != "Oscuro":
        return
    try:
        import ctypes
        root.update_idletasks()
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        val = ctypes.c_int(1)
        for attr in (20, 19):             # DWMWA_USE_IMMERSIVE_DARK_MODE (Win10 antiguo usa 19)
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, attr, ctypes.byref(val), ctypes.sizeof(val))
    except Exception:  # noqa: BLE001
        pass

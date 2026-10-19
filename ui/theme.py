"""Tema visual (ttk 'clam' personalizado): colores, fuentes y estilos."""
import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk

PRIMARY = "#0F6E7C"
PRIMARY_DARK = "#0A525D"
PRIMARY_LIGHT = "#E3F1F4"
BG = "#F3F6F7"
CARD = "#FFFFFF"
TEXT = "#1F2A30"
MUTED = "#5F6B70"
BORDER = "#C5D1D6"
DANGER = "#B3261E"
WARN = "#9A5B00"
WARN_BG = "#FFF3D6"
OK = "#1B7F4B"
OK_BG = "#DDF3E6"
SIDEBAR = "#0B3C45"
SIDEBAR_HOVER = "#12525D"
SUGGEST_BG = "#FFFBEA"

FAMILY = "TkDefaultFont"
FONT = (FAMILY, 11)
FONT_B = (FAMILY, 11, "bold")
FONT_H1 = (FAMILY, 20, "bold")
FONT_H2 = (FAMILY, 14, "bold")
FONT_SMALL = (FAMILY, 9)
FONT_TEXT = (FAMILY, 11)
FONT_BIG = (FAMILY, 30, "bold")


def _pick_family(root):
    available = {f.lower(): f for f in tkfont.families(root)}
    for name in ("Segoe UI", "Helvetica Neue", "Noto Sans", "DejaVu Sans", "Liberation Sans",
                 "Arial", "Helvetica"):
        if name.lower() in available:
            return available[name.lower()]
    return "TkDefaultFont"


def setup(root: tk.Tk):
    global FAMILY, FONT, FONT_B, FONT_H1, FONT_H2, FONT_SMALL, FONT_TEXT, FONT_BIG
    FAMILY = _pick_family(root)
    FONT = (FAMILY, 11)
    FONT_B = (FAMILY, 11, "bold")
    FONT_H1 = (FAMILY, 20, "bold")
    FONT_H2 = (FAMILY, 14, "bold")
    FONT_SMALL = (FAMILY, 9)
    FONT_TEXT = (FAMILY, 11)
    FONT_BIG = (FAMILY, 30, "bold")

    for name in ("TkDefaultFont", "TkTextFont", "TkMenuFont", "TkHeadingFont", "TkCaptionFont",
                 "TkTooltipFont"):
        try:
            tkfont.nametofont(name).configure(family=FAMILY, size=11)
        except tk.TclError:
            pass
    root.configure(bg=BG)
    root.option_add("*TCombobox*Listbox.font", FONT)
    root.option_add("*TCombobox*Listbox.selectBackground", PRIMARY)

    s = ttk.Style(root)
    s.theme_use("clam")
    s.configure(".", background=BG, foreground=TEXT, font=FONT, bordercolor=BORDER,
                lightcolor=BG, darkcolor=BG, troughcolor="#E4EAEC", focuscolor=PRIMARY)

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
    s.configure("H1.TLabel", font=FONT_H1, foreground=PRIMARY_DARK)
    s.configure("H2.TLabel", font=FONT_H2, foreground=PRIMARY_DARK)
    s.configure("Field.TLabel", font=(FAMILY, 10, "bold"), foreground=MUTED)
    s.configure("CardField.TLabel", font=(FAMILY, 10, "bold"), foreground=MUTED, background=CARD)
    s.configure("StatNum.TLabel", font=FONT_BIG, foreground=PRIMARY, background=CARD)
    s.configure("StatCap.TLabel", font=FONT_B, foreground=MUTED, background=CARD)
    s.configure("StatSub.TLabel", font=FONT_SMALL, foreground=MUTED, background=CARD)
    s.configure("SidebarTitle.TLabel", background=SIDEBAR, foreground="white", font=(FAMILY, 13, "bold"))
    s.configure("SidebarSub.TLabel", background=SIDEBAR, foreground="#9CC4CB", font=FONT_SMALL)
    s.configure("Draft.TLabel", background=WARN_BG, foreground=WARN, font=FONT_B, padding=(10, 4))
    s.configure("Final.TLabel", background=OK_BG, foreground=OK, font=FONT_B, padding=(10, 4))
    s.configure("Dirty.TLabel", foreground=DANGER, font=FONT_B)
    s.configure("Saved.TLabel", foreground=OK, font=FONT_B)
    s.configure("Warn.TLabel", foreground=WARN, font=FONT_B)
    s.configure("Error.TLabel", foreground=DANGER, font=FONT_B)

    s.configure("TButton", padding=(14, 7), font=FONT, background="#E6ECEE", foreground=TEXT,
                bordercolor=BORDER, relief="flat", focusthickness=2, width=0)
    s.map("TButton", background=[("disabled", "#EEF1F2"), ("active", "#D5DFE2")],
          foreground=[("disabled", "#9AA5A9")])
    s.configure("Accent.TButton", background=PRIMARY, foreground="white", font=FONT_B,
                bordercolor=PRIMARY_DARK)
    s.map("Accent.TButton", background=[("disabled", "#9DBFC5"), ("active", PRIMARY_DARK)],
          foreground=[("disabled", "#F0F5F6")])
    s.configure("Danger.TButton", background="#F8E3E1", foreground=DANGER, font=FONT_B)
    s.map("Danger.TButton", background=[("disabled", "#F4ECEB"), ("active", "#F1CBC7")])
    s.configure("Small.TButton", padding=(8, 3), font=(FAMILY, 10))
    s.configure("Nav.TButton", background=SIDEBAR, foreground="white", anchor="w", padding=(18, 11),
                font=FONT, relief="flat", borderwidth=0)
    s.map("Nav.TButton", background=[("active", SIDEBAR_HOVER)])
    s.configure("NavActive.TButton", background=PRIMARY, foreground="white", anchor="w",
                padding=(18, 11), font=FONT_B, relief="flat", borderwidth=0)
    s.map("NavActive.TButton", background=[("active", PRIMARY)])
    s.configure("Strip.TButton", background="#FFFFFF", padding=(10, 5), font=(FAMILY, 10, "bold"))
    s.map("Strip.TButton", background=[("active", "#D5E8EC")])

    s.configure("TEntry", fieldbackground="white", padding=6, bordercolor=BORDER, lightcolor="white",
                darkcolor="white")
    s.map("TEntry", bordercolor=[("focus", PRIMARY)], fieldbackground=[("disabled", "#EDF0F1"),
                                                                       ("readonly", "#EDF0F1")])
    s.configure("Bad.TEntry", fieldbackground="#FDECEA", foreground=DANGER, padding=6,
                bordercolor=DANGER, lightcolor="#FDECEA", darkcolor="#FDECEA")
    s.configure("Hint.TLabel", foreground=MUTED, font=FONT_SMALL)
    s.configure("Note.TLabel", foreground=WARN, background=WARN_BG, font=FONT, padding=(10, 6))
    s.configure("TCombobox", fieldbackground="white", padding=6, bordercolor=BORDER,
                lightcolor="white", darkcolor="white", arrowsize=16, background="#E6ECEE")
    s.map("TCombobox", bordercolor=[("focus", PRIMARY)],
          fieldbackground=[("disabled", "#EDF0F1"), ("readonly", "white")],
          foreground=[("disabled", "#7C878B")])
    s.configure("TCheckbutton", background=BG, font=FONT)
    s.configure("Card.TCheckbutton", background=CARD)
    s.configure("TRadiobutton", background=BG, font=FONT)
    s.configure("Card.TRadiobutton", background=CARD)

    s.configure("TNotebook", background=BG, borderwidth=0, tabmargins=(0, 4, 0, 0))
    s.configure("TNotebook.Tab", padding=(14, 8), font=FONT_B, background="#DCE5E8", foreground=MUTED,
                bordercolor=BORDER)
    s.map("TNotebook.Tab", background=[("selected", CARD)], foreground=[("selected", PRIMARY_DARK)],
          expand=[("selected", (0, 2, 0, 0))])

    s.configure("Treeview", rowheight=30, font=FONT, background="white", fieldbackground="white",
                bordercolor=BORDER)
    s.configure("Treeview.Heading", font=FONT_B, background=PRIMARY_LIGHT, foreground=PRIMARY_DARK,
                padding=(8, 7), relief="flat")
    s.map("Treeview.Heading", background=[("active", "#CFE6EA")])
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

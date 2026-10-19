# -*- mode: python ; coding: utf-8 -*-
# Generado a mano para PyInstaller. Uso:  pyinstaller --noconfirm --clean BrigadasMedicas.spec
block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[],
    hiddenimports=[
        'ui.page_home', 'ui.page_patient', 'ui.page_search', 'ui.page_visit', 'ui.page_history',
        'ui.page_brigades', 'ui.page_ata', 'services.ata', 'ui.page_reports', 'ui.page_backup', 'ui.page_settings',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=['matplotlib', 'numpy', 'pandas', 'scipy'],
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz, a.scripts, [],
    exclude_binaries=True,
    name='BrigadasMedicas',
    debug=False,
    strip=False,
    upx=False,
    console=False,          # sin ventana de consola
)
coll = COLLECT(exe, a.binaries, a.zipfiles, a.datas, strip=False, upx=False, name='BrigadasMedicas')

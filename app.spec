# -*- mode: python ; coding: utf-8 -*-

# --- CÓDIGO AÑADIDO ---
import os

# ¡RUTA CORREGIDA CON DOBLES BARRAS INVERTIDAS (\\) EN TODA LA LÍNEA!
ruta_mediapipe = 'c:\\users\\usuario\\appdata\\local\\programs\\python\\python310\\lib\\site-packages\\mediapipe'

mediapipe_files = [
    (os.path.join(ruta_mediapipe, 'modules'), 'mediapipe/modules'),
]
# --- FIN DEL CÓDIGO AÑADIDO ---

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    # MODIFICA ESTA LÍNEA PARA AÑADIR '+ mediapipe_files'
    datas=[('templates', 'templates'), ('static', 'static')] + mediapipe_files,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['src\\cracken-gui.py'],
    pathex=['.\\src'],
    binaries=[],
    datas=[
        ('src\\resources\\logo.png', '.\\resources'), 
        ('src\\ui\\images\\close.png', '.\\ui\\images'), 
        ('src\\renpy', '.\\renpy')
    ],
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
    name='renpy-cracken',
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
    icon=['src\\resources\\icon.ico'],
)

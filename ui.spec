# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['ui\\ui.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('ui\\images\\logo.png', '.\\images'), 
        ('ui\\images\\close.png', '.\\images'), 
        ('renpy\\display', '.\\renpy\\display'), 
        ('renpy\\sl2', '.\\renpy\\sl2'), 
        ('renpy\\text', '.\\renpy\\text'), 
        ('renpy\\__init__.py', '.\\renpy'), 
        ('renpy\\ast.py', '.\\renpy'), 
        ('renpy\\atl.py', '.\\renpy'), 
        ('renpy\\object.py', '.\\renpy'), 
        ('renpy\\parameter.py', '.\\renpy'), 
        ('renpy\\python.py', '.\\renpy'), 
        ('renpy\\ui.py', '.\\renpy')
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
    name='ui',
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
    icon=['ui\\icon.ico'],
)

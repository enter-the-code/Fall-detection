# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['decode.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('img/bm_icon.ico','.'),
        ('C:/Users/Corsair/anaconda3/Library/bin/mkl_intel_thread.2.dll','.'),
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
    name='6843ISK csv Converter',
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
    icon='.\\img\\bm_icon.ico',
)

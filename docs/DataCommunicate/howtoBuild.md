# How to Build

## pyinstaller 설치
```cmd
pip install pyinstaller
```
* dependency check 위한 빌드 이전 최신화 필요

## 초기 빌드
```cmd
pyinstaller --onefile --windowed -n "FnDigitEncoder" FnDigitEncoder.py  
```

### 다시 빌드
spec 변경에 따라 다시 빌드하기는
```cmd
pyinstaller app.spec
```

### exe파일의 icon 설정
exe = EXE(... icon='path') 명시

## spec 파일
```py
a = Analysis(
    ['app.py'],  # main script
    pathex=[],  # additional paths to include for module searching
    binaries=[],    # extra binary files like DLLs
    datas=[],   # extra images like images or configs
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
    name='app_name',  # name of output file
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,   # UPX compress
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # disable console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
```
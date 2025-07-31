# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py', 'categories.py', 'programs.py'],
    pathex=[],
    binaries=[],
    datas=[('categories.py', '.'), ('programs.py', '.')],
    hiddenimports=['bs4', 'lxml', 'html5lib', 'categories', 'programs', 'selenium', 'selenium.webdriver', 'selenium.webdriver.chrome', 'selenium.webdriver.chrome.options', 'selenium.webdriver.support', 'selenium.webdriver.common.by', 'selenium.webdriver.support.expected_conditions', 'urllib.robotparser', 'pathlib'],
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
    name='u-crawler',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

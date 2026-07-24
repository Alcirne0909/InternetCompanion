# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('BolaBuddy1.png', '.'), ('BolaBuddy1Falando.png', '.'), ('BolaBuddyAssustador.png', '.'), ('BolaBuddyFesta.png', '.'), ('wallpapers', 'wallpapers'), ('Musicas', 'Musicas'), ('dangarompaWallpapers', 'dangarompaWallpapers'), ('Rodando', 'Rodando')],
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
    name='main',
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

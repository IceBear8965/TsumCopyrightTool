# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['TsumCopyrightTool.py'],
    pathex=[],
    binaries=[],
    datas=[
    ('app/resources/', 'app/resources/'),
    ('app/common/', 'app/common/'),
    ('app/components/', 'app/components/'),
    ('app/view/', 'app/view/'),
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
    [],
    exclude_binaries=True,
    name='TsumCopyrightTool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app/resources/images/tsumlogo.ico',
    contents_directory='.',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='TsumCopyrightTool',
)

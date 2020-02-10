# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

src_dir="/root/source/54testframework/"
a = Analysis(['main.py','modules/ecom_ns_2/ecom_ns2_test_process.py'],
             pathex=['/root/source/54testframework'],
             binaries=[],
             datas=[(src_dir+'logs','logs'),(src_dir+'imgs','imgs'),(src_dir+'langs','langs'),(src_dir+'conf','conf')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='test_system',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='test_system')

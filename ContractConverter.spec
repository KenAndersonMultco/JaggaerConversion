# -*- mode: python -*-

block_cipher = None


a = Analysis(['ContractConverter.py'],
             pathex=['C:\\Users\\anderskr\\github\\JaggaerConversion'],
             binaries=[],
             datas=[('AppData\\rules.csv', 'appdata'), ('h:\\JaggaerDC\\AppData\\JaggaerUsers.csv', 'appdata'), ('AppData\\Nicknames.csv', 'appdata'), ('AppData\\ContractType.csv', 'appdata'), ('AppData\\Status.csv', 'appdata'), ('AppData\\Suppliers.csv', 'appdata'), ('AppData\\projects.csv', 'appdata')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='ContractConverter',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='ContractConverter')

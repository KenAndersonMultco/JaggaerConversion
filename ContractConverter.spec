# -*- mode: python -*-

block_cipher = None


a = Analysis(['ContractConverter.py'],
             pathex=['c:\\Users\\anderskr\\github\\JaggaerConversion'],
             binaries=[],
             datas=[('h:\\JaggaerDC\\AppData\\rules.csv', 'appdata'), ('h:\\JaggaerDC\\AppData\\MultcoUsers.csv', 'appdata'), ('h:\\JaggaerDC\\AppData\\JaggaerUsers.csv', 'appdata'), ('h:\\JaggaerDC\\AppData\\Nicknames.csv', 'appdata'), ('h:\\JaggaerDC\\AppData\\ContractType.csv', 'appdata'), ('h:\\JaggaerDC\\AppData\\Status.csv', 'appdata'), ('h:\\JaggaerDC\\AppData\\Suppliers.csv', 'appdata'), ('h:\\JaggaerDC\\AppData\\projects.csv', 'appdata')],
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

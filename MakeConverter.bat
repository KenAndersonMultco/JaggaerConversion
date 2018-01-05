::echo off
cd c:\Users\anderskr\github\JaggaerConversion
::pyinstaller --noconfirm --log-level=WARN ^
::  --windowed ^
::  --add-data="h:\JaggaerDC\MultcoUsers.csv;appdata" ^
::  ContractConverter.py
pyinstaller --windowed --noconfirm ^
--add-data="h:\JaggaerDC\AppData\rules.csv;appdata" ^
--add-data="h:\JaggaerDC\AppData\MultcoUsers.csv;appdata" ^
--add-data="h:\JaggaerDC\AppData\JaggaerUsers.csv;appdata" ^
--add-data="h:\JaggaerDC\AppData\Nicknames.csv;appdata" ^
--add-data="h:\JaggaerDC\AppData\ContractType.csv;appdata" ^
--add-data="h:\JaggaerDC\AppData\Status.csv;appdata" ^
--add-data="h:\JaggaerDC\AppData\Suppliers.csv;appdata" ^
--add-data="h:\JaggaerDC\AppData\projects.csv;appdata" ^
ContractConverter.py

  
	
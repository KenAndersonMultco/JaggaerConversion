::echo off
::cd c:\Users\anderskr\github\JaggaerConversion
::pyinstaller --noconfirm --log-level=WARN ^
::  --windowed ^
::  --add-data="h:\JaggaerDC\MultcoUsers.csv;appdata" ^
::  ContractConverter.py
pyinstaller --windowed --noconfirm  ^
--add-data="AppData\rules.csv;appdata" ^
--add-data="h:\JaggaerDC\AppData\JaggaerUsers.csv;appdata" ^
--add-data="AppData\Nicknames.csv;appdata" ^
--add-data="AppData\ContractType.csv;appdata" ^
--add-data="AppData\Status.csv;appdata" ^
--add-data="AppData\Suppliers.csv;appdata" ^
--add-data="AppData\projects.csv;appdata" ^
ContractConverter.py

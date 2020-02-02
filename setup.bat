xcopy /S/E/V/H .\HVB-Kassesystem "C:\Program Files\HVB-Kassesystem\"
powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%userprofile%\Desktop\Kassesystem.lnk');$s.TargetPath='python.exe';$s.Arguments =\"`\"C:\Program Files\HVB-Kassesystem\main.py`\"\";$s.Save()"

IF EXIST "C:\Program Files\HVB-Kassesystem\statistics\location.txt" DEL /F "C:\Program Files\HVB-Kassesystem\statistics\location.txt"
echo %UserProfile%\Documents\Kassesystem_log\>>"C:\Program Files\HVB-Kassesystem\statistics\location.txt"

pip install -r "C:\Program Files\HVB-Kassesystem\requirements.txt"
node "C:\Program Files\HVB-Kassesystem\install.js"
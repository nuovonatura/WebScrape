Write-Output Installing Python 3
winget install --id Python.Python.3 --source winget -i
PAUSE
$file = (Get-Location).toString() + "\Setup.ps1"
$argsLst = '-NoProfile -ExecutionPolicy Unrestricted -File ""' + $file + '""'
Start-Process PowerShell -ArgumentList $argsLst -Verb RunAs
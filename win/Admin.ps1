$file = (Get-Location).toString() + "\Setup.ps1"
$argsLst = '-NoProfile -ExecutionPolicy Unrestricted -File ""' + $file + '""'
Start-Process PowerShell -ArgumentList $argsLst -Verb RunAs
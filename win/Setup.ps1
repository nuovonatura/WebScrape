Write-Host "Checking for elevated permissions..."
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole(`
    [Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Warning "Insufficient permissions to run this script. Open the PowerShell console as an administrator and run this script again."
    PAUSE
    Break
}
else {
    Write-Host "Code is running as administrator — go on executing the script..." -ForegroundColor Green
}
Write-Progress -Activity Installing required modules... -PercentComplete 0
Write-Progress -CurrentOperation Installing Python 3
winget install --id Python.Python.3 --source winget -i
PAUSE
Write-Progress -CurrentOperation Installing Python Selenium -PercentComplete 50
pip install selenium
PAUSE
Write-Progress -CurrentOperation Installing Python Pandas -PercentComplete 80
pip install pandas
PAUSE
Write-Progress -CurrentOperation Installing Python numpy -PercentComplete 95
pip install numpy
Write-Progress -Completed
PAUSE
Break
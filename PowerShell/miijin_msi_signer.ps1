# This file is used to sign an MSI package using a self-signed certificate and the signtool
# Signtool can be acquired from the Windows SDK
# This file assumes your certs are in C:\Temp
# It also assumes that you copied your MSIs to C:\Temp

$fileName = Read-Host -Prompt "Provide the filename that you called your certs and keys"
$password = Read-Host -Prompt "Provide the password you used when generating the certs/keys"
$description = Read-Host -Prompt "Provide a brief description of what the MSI does"

$miijinmsi = Read-Host -Prompt "Enter the name of the MSI file (if you have spaces remove them and include the extension)"

$signtoolDir = "C:\Program Files (x86)\Microsoft SDKs\ClickOnce\SignTool"
Set-Location -Path $signtoolDir

Start-Process .\signtool.exe -Argumentlist "sign /f C:\Temp\$fileName.p12 /p $password /d '$description' /tr http://timestamp.digicert.com /v C:\Temp\$miijinmsi" -Wait
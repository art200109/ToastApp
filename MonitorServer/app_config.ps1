$app_path = "$PSScriptRoot\FlaskApp"

. $PSScriptRoot\..\General_Scripts\InstallFlaskIIS.ps1

. $PSScriptRoot\..\General_Scripts\InstallAgent.ps1

pip install -r .\API\requirments.txt

. $PSScriptRoot\..\General_Scripts\InstallNSSM.ps1

Config-NSSM -serviceName "Sblunk" -appPath $(Resolve-Path ".\API\api_server.py").path
Start-Service Sblunk
Set-Service -StartupType Automatic "Sblunk"

ConvertTo-WebApplication -PSPath 'IIS:\Sites\Default Web Site\assets'
Remove-WebHandler FlaskHandler -PSPath 'IIS:\Sites\Default Web Site\assets'

. $PSScriptRoot\..\General_Scripts\ChangeRDP.ps1
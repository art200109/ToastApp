$app_path = "$PSScriptRoot\FlaskApp"

. $PSScriptRoot\..\General_Scripts\InstallFlaskIIS.ps1

. $PSScriptRoot\..\General_Scripts\InstallNSSM.ps1

ConvertTo-WebApplication -PSPath 'IIS:\Sites\Default Web Site\assets'
Remove-WebHandler FlaskHandler -PSPath 'IIS:\Sites\Default Web Site\assets'

Config-NSSM -serviceName "Sflunk" -appPath $(Resolve-Path ".\API\api_server.py").path

. $PSScriptRoot\..\General_Scripts\ChangeRDP.ps1
$app_path = "$PSScriptRoot\FlaskApp"

. $PSScriptRoot\..\General_Scripts\InstallFlaskIIS.ps1

. $PSScriptRoot\..\General_Scripts\InstallNSSM.ps1

Config-NSSM -serviceName "Sflunk" -appPath $(Resolve-Path ".\API\api_server.py").path

. $PSScriptRoot\..\General_Scripts\ChangeRDP.ps1
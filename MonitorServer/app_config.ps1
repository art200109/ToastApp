$app_path = "C:\inetpub\www\ToastApp\MonitorServer\FlaskApp"

. $PSScriptRoot\..\General_Scripts\InstallFlaskIIS.ps1

. $PSScriptRoot\..\General_Scripts\InstallAgent.ps1

C:\Python\python.exe -m pip install -r .\API\requirements.txt

. $PSScriptRoot\..\General_Scripts\InstallNSSM.ps1

Config-NSSM -serviceName "Sblunk" -appPath "C:\inetpub\www\ToastApp\MonitorServer\API\api_server.py"
Start-Service Sblunk
Set-Service -StartupType Automatic "Sblunk"

ConvertTo-WebApplication -PSPath 'IIS:\Sites\Default Web Site\assets'
Remove-WebHandler FlaskHandler -PSPath 'IIS:\Sites\Default Web Site\assets'

. $PSScriptRoot\..\General_Scripts\ChangeRDP.ps1

Read-Host "Finish..."
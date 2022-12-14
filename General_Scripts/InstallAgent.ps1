pip install -r ..\MonitoringAgent\requirements.txt

. $PSScriptRoot\InstallNSSM.ps1

Config-NSSM -serviceName "SblunkForwarder" -appPath $(Resolve-Path "..\MonitoringAgent\app.py").path
Start-Service SblunkForwarder
Set-Service -StartupType Automatic "SblunkForwarder"
C:\Python\python.exe -m pip install -r $PSScriptRoot\..\MonitoringAgent\requirements.txt

. $PSScriptRoot\InstallNSSM.ps1

Copy-Item $PSScriptRoot\..\MonitoringAgent\conf_backup\original_agent.conf.backup  $PSScriptRoot\..\MonitoringAgent\agent.conf -Force

Config-NSSM -serviceName "SblunkForwarder" -appPath "C:\inetpub\wwwroot\ToastApp\MonitoringAgent\app.py"
Start-Service SblunkForwarder
Set-Service -StartupType Automatic "SblunkForwarder"
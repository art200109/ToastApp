C:\Python\python.exe -m pip install -r $PSScriptRoot\..\MonitoringAgent\requirements.txt

. $PSScriptRoot\InstallNSSM.ps1

Config-NSSM -serviceName "SblunkForwarder" -appPath "C:\inetpub\wwwroot\ToastApp\MonitoringAgent\app.py"
Start-Service SblunkForwarder
Set-Service -StartupType Automatic "SblunkForwarder"
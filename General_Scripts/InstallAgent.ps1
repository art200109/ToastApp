C:\Python\python.exe -m pip install -r ..\MonitoringAgent\requirements.txt

. $PSScriptRoot\InstallNSSM.ps1

Config-NSSM -serviceName "SblunkForwarder" -appPath "C:\inetpub\www\ToastApp\MonitoringAgent\app.py"
Start-Service SblunkForwarder
Set-Service -StartupType Automatic "SblunkForwarder"
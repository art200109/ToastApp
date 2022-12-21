Invoke-WebRequest -Uri "https://nssm.cc/release/nssm-2.24.zip" -OutFile "c:\temp\nssm.zip"
Expand-Archive C:\temp\nssm.zip -DestinationPath C:\temp\nssm -Force
C:\temp\nssm\nssm-2.24\win64\nssm.exe install ToastAgentArtume "C:\Python\python.exe" "C:\temp\ToastApp\MonitoringAgent\app.py"
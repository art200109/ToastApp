Invoke-WebRequest -Uri "https://github.com/minishift/minishift/releases/download/v1.34.3/minishift-1.34.3-windows-amd64.zip" -OutFile "c:/temp/minishift.zip"
Expand-Archive C:\temp\minishift.zip -DestinationPath C:\temp\

C:\temp\minishift-1.34.3-windows-amd64\minishift.exe config unset vm-driver virtualbox
C:\temp\minishift-1.34.3-windows-amd64\minishift.exe start 
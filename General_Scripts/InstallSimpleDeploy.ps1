# Invoke-WebRequest -Uri "https://github.com/jesperhoy/SimpleDeploy/releases/download/v0.9.1/SimpleDeploy-0.9.1.zip" -OutFile "c:/temp/deploy.zip"
# Expand-Archive C:\temp\deploy.zip -DestinationPath C:\inetpub\wwwroot\SimpleDeploy
Copy-Item C:\temp\ToastApp\SimpleDeploy C:\inetpub\wwwroot -Force -Recurse
New-WebSite -Name "SimpleDeploy" -Port 1234 -PhysicalPath "C:\inetpub\wwwroot\SimpleDeploy"
Remove-WebHandler FlaskHandler -PSPath 'IIS:\Sites\SimpleDeploy'
icacls C:\inetpub\wwwroot\SimpleDeploy /grant "NT AUTHORITY\IUSR:(OI)(CI)F" /T
icacls C:\inetpub\wwwroot\SimpleDeploy /grant "Builtin\IIS_IUSRS:(OI)(CI)F" /T
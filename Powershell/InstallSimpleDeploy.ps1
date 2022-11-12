Invoke-WebRequest -Uri "https://github.com/jesperhoy/SimpleDeploy/releases/download/v0.9.1/SimpleDeploy-0.9.1.zip" -OutFile "c:/temp/deploy.zip"
Expand-Archive C:\temp\deploy.zip -DestinationPath C:\inetpub\wwwroot\SimpleDeploy
New-WebSite -Name "SimpleDeploy" -Port 1234 -PhysicalPath "C:\inetpub\wwwroot\SimpleDeploy"
Remove-WebHandler FlaskHandler -PSPath 'IIS:\Sites\SimpleDeploy'
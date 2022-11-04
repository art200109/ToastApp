﻿[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
if (-not (Test-Path C:\temp))
{
    New-Item -ItemType Directory C:\temp
}


Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.7.0/python-3.7.0.exe" -OutFile "c:/temp/python-3.7.0.exe"

c:/temp/python-3.7.0.exe /q InstallAllUsers=1 PrependPath=1 TargetDir="C:\Python"

C:\Python\python.exe -m pip install --upgrade pip

C:\Python\python.exe -m pip install flask
C:\Python\python.exe -m pip install wfastcgi --use-pep517
C:\Python\python.exe -m pip install pymongo

Enable-WindowsOptionalFeature -FeatureName IIS-WebServerRole -Online
Enable-WindowsOptionalFeature -FeatureName IIS-CGI -Online

C:\Python\Scripts\wfastcgi-enable.exe

#Copy-Item C:\Python\Lib\site-packages\wfastcgi.py C:\inetpub\wwwroot\FlaskApp\

icacls C:\inetpub\wwwroot\ToastApp /grant "NT AUTHORITY\IUSR:(OI)(CI)(RX)"
icacls C:\inetpub\wwwroot\ToastApp /grant "Builtin\IIS_IUSRS:(OI)(CI)(RX)"

Set-ItemProperty 'IIS:\Sites\Default Web Site' -name physicalPath -value "C:\inetpub\wwwroot\ToastApp\AppServer\FlaskApp"

New-WebHandler -Name FlaskHandler -Path * -Verb * -Modules FastCgiModule -ScriptProcessor "C:\Python\python.exe|C:\inetpub\wwwroot\ToastApp\AppServer\FlaskApp\wfastcgi.py" -Type $null -Force

$python = "C:\inetpub\wwwroot\ToastApp\AppServer\FlaskApp"

$configPath = "system.webServer/fastCgi/application[@arguments='$($python+"\wfastcgi.py")']/environmentVariables/environmentVariable"
$config = Get-WebConfiguration $configPath
if (!$config) {
    Add-WebConfiguration $configPath -Value @{ 'Name' = 'PYTHONPATH'; Value = "$python" }
    Add-WebConfiguration $configPath -Value @{ 'Name' = 'WSGI_HANDLER'; Value = "app.app" }
}

ConvertTo-WebApplication -PSPath 'IIS:\Sites\Default Web Site\assets'
Remove-WebHandler FlaskHandler -PSPath 'IIS:\Sites\Default Web Site\assets'

iisreset
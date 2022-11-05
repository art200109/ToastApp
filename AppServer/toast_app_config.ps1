[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
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
C:\Python\python.exe -m pip install requests

Enable-WindowsOptionalFeature -Online -FeatureName IIS-WebServerRole
Enable-WindowsOptionalFeature -Online -FeatureName IIS-WebServer
Enable-WindowsOptionalFeature -Online -FeatureName IIS-CommonHttpFeatures
Enable-WindowsOptionalFeature -Online -FeatureName IIS-HttpErrors
Enable-WindowsOptionalFeature -Online -FeatureName IIS-HttpRedirect
Enable-WindowsOptionalFeature -Online -FeatureName IIS-ApplicationDevelopment

Enable-WindowsOptionalFeature -online -FeatureName NetFx4Extended-ASPNET45
Enable-WindowsOptionalFeature -Online -FeatureName IIS-NetFxExtensibility45

Enable-WindowsOptionalFeature -Online -FeatureName IIS-HealthAndDiagnostics
Enable-WindowsOptionalFeature -Online -FeatureName IIS-HttpLogging
Enable-WindowsOptionalFeature -Online -FeatureName IIS-LoggingLibraries
Enable-WindowsOptionalFeature -Online -FeatureName IIS-RequestMonitor
Enable-WindowsOptionalFeature -Online -FeatureName IIS-HttpTracing
Enable-WindowsOptionalFeature -Online -FeatureName IIS-Security
Enable-WindowsOptionalFeature -Online -FeatureName IIS-RequestFiltering
Enable-WindowsOptionalFeature -Online -FeatureName IIS-Performance
Enable-WindowsOptionalFeature -Online -FeatureName IIS-WebServerManagementTools
Enable-WindowsOptionalFeature -Online -FeatureName IIS-IIS6ManagementCompatibility
Enable-WindowsOptionalFeature -Online -FeatureName IIS-Metabase
Enable-WindowsOptionalFeature -Online -FeatureName IIS-ManagementConsole
Enable-WindowsOptionalFeature -Online -FeatureName IIS-BasicAuthentication
Enable-WindowsOptionalFeature -Online -FeatureName IIS-StaticContent
Enable-WindowsOptionalFeature -Online -FeatureName IIS-DefaultDocument
Enable-WindowsOptionalFeature -Online -FeatureName IIS-WebSockets
Enable-WindowsOptionalFeature -Online -FeatureName IIS-ApplicationInit
Enable-WindowsOptionalFeature -Online -FeatureName IIS-ISAPIExtensions
Enable-WindowsOptionalFeature -Online -FeatureName IIS-ISAPIFilter
Enable-WindowsOptionalFeature -Online -FeatureName IIS-HttpCompressionStatic

Enable-WindowsOptionalFeature -Online -FeatureName IIS-ASPNET45

Enable-WindowsOptionalFeature -FeatureName IIS-CGI -Online

Import-Module WebAdministration

C:\Python\Scripts\wfastcgi-enable.exe

#Copy-Item C:\Python\Lib\site-packages\wfastcgi.py C:\inetpub\wwwroot\FlaskApp\

icacls C:\inetpub\wwwroot\ToastApp /grant "NT AUTHORITY\IUSR:(OI)(CI)(RX)"
icacls C:\inetpub\wwwroot\ToastApp /grant "Builtin\IIS_IUSRS:(OI)(CI)(RX)"

Set-ItemProperty 'IIS:\Sites\Default Web Site' -name physicalPath -value "C:\inetpub\wwwroot\ToastApp\AppServer\FlaskApp"

New-WebHandler -Name FlaskHandler -Path * -Verb * -Modules FastCgiModule -ScriptProcessor "C:\Python\python.exe|C:\inetpub\wwwroot\ToastApp\AppServer\FlaskApp\wfastcgi.py" -Type $null -Force

$python = "C:\inetpub\wwwroot\ToastApp\AppServer\FlaskApp"

$configPath = "system.webServer/fastCgi/application[@arguments='$($python+"\wfastcgi.py")']/environmentVariables/PYTHONPATH"
$config = Get-WebConfiguration $configPath
if (!$config) {
    Add-WebConfiguration $configPath -Value @{ 'Name' = 'PYTHONPATH'; Value = "$python" }
    Add-WebConfiguration $configPath -Value @{ 'Name' = 'WSGI_HANDLER'; Value = "app.app" }
}

ConvertTo-WebApplication -PSPath 'IIS:\Sites\Default Web Site\assets'
Remove-WebHandler FlaskHandler -PSPath 'IIS:\Sites\Default Web Site\assets'

iisreset

Invoke-WebRequest -Uri "https://github.com/minishift/minishift/releases/download/v1.34.3/minishift-1.34.3-windows-amd64.zip" -OutFile "c:/temp/minishift.zip"
Expand-Archive C:\temp\minishift.zip -DestinationPath C:\temp\

C:\temp\minishift-1.34.3-windows-amd64\minishift.exe config unset vm-driver virtualbox
C:\temp\minishift-1.34.3-windows-amd64\minishift.exe start 
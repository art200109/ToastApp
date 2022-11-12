[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
if (-not (Test-Path C:\temp))
{
    New-Item -ItemType Directory C:\temp
}


Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.7.0/python-3.7.0.exe" -OutFile "c:/temp/python-3.7.0.exe"

Start-Process -FilePath c:/temp/python-3.7.0.exe -ArgumentList '/q InstallAllUsers=1 PrependPath=1 TargetDir="C:\Python"' -NoNewWindow -Wait

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
Enable-WindowsOptionalFeature -Online -FeatureName IIS-CGI


cd C:\inetpub\wwwroot
git clone https://github.com/art200109/ToastApp.git

Import-Module WebAdministration

C:\Python\Scripts\wfastcgi-enable.exe

#Copy-Item C:\Python\Lib\site-packages\wfastcgi.py C:\inetpub\wwwroot\FlaskApp\

icacls C:\inetpub\wwwroot\ToastApp /grant "NT AUTHORITY\IUSR:(OI)(CI)(RX)"
icacls C:\inetpub\wwwroot\ToastApp /grant "Builtin\IIS_IUSRS:(OI)(CI)(RX)"

Set-ItemProperty 'IIS:\Sites\Default Web Site' -name physicalPath -value "C:\inetpub\wwwroot\ToastApp\AppServer\FlaskApp"

New-WebHandler -Name FlaskHandler -Path * -Verb * -Modules FastCgiModule -ScriptProcessor "C:\Python\python.exe|C:\inetpub\wwwroot\ToastApp\AppServer\FlaskApp\wfastcgi.py" -Type $null -Force

$python = "C:\inetpub\wwwroot\ToastApp\AppServer\FlaskApp"

$configPath = "/system.webServer/fastCgi/application[@fullPath='C:\Python\python.exe']" 
Set-WebConfigurationProperty $configPath -Name arguments -Value $python\wfastcgi.py

Add-WebConfiguration $configPath/environmentVariables -Value @{ 'Name' = 'PYTHONPATH'; Value = "$python" }
Add-WebConfiguration $configPath/environmentVariables -Value @{ 'Name' = 'WSGI_HANDLER'; Value = "app.app" }

ConvertTo-WebApplication -PSPath 'IIS:\Sites\Default Web Site\assets'
Remove-WebHandler FlaskHandler -PSPath 'IIS:\Sites\Default Web Site\assets'

iisreset
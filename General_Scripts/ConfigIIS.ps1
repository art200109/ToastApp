$features = @(
    "IIS-WebServerRole",
    "IIS-WebServer",
    "IIS-CommonHttpFeatures",
    "IIS-HttpErrors",
    "IIS-HttpRedirect",
    "IIS-ApplicationDevelopment",
    "NetFx4Extended-ASPNET45",
    "IIS-NetFxExtensibility45",
    "IIS-HealthAndDiagnostics",
    "IIS-HttpLogging",
    "IIS-LoggingLibraries",
    "IIS-RequestMonitor",
    "IIS-HttpTracing",
    "IIS-Security",
    "IIS-RequestFiltering",
    "IIS-Performance",
    "IIS-WebServerManagementTools",
    "IIS-IIS6ManagementCompatibility",
    "IIS-Metabase",
    "IIS-ManagementConsole",
    "IIS-BasicAuthentication",
    "IIS-StaticContent",
    "IIS-DefaultDocument",
    "IIS-WebSockets",
    "IIS-ApplicationInit",
    "IIS-ISAPIExtensions",
    "IIS-ISAPIFilter",
    "IIS-HttpCompressionStatic",
    "IIS-ASPNET45",
    "IIS-CGI"
)

foreach($feature in $features) 
{ 
    if($(get-WindowsOptionalFeature -Online -FeatureName $feature).State -ne "Enabled")
    {
        Enable-WindowsOptionalFeature -Online -FeatureName $feature 
    }
    Write-host "$feature - Installed" -foreground Green
}

if(-not $(Test-Path C:\inetpub\wwwroot\ToastApp))
{
    cd C:\inetpub\wwwroot
    git clone https://github.com/art200109/ToastApp.git
}
icacls C:\inetpub\wwwroot\ToastApp /grant "NT AUTHORITY\IUSR:(OI)(CI)(RX)"
icacls C:\inetpub\wwwroot\ToastApp /grant "Builtin\IIS_IUSRS:(OI)(CI)(RX)"

C:\Python\Scripts\wfastcgi-enable.exe
###Copy-Item C:\Python\Lib\site-packages\wfastcgi.py C:\inetpub\wwwroot\FlaskApp\

Import-Module WebAdministration

$wfast_path = "C:\inetpub\wwwroot\ToastApp\General_Scripts\wfastcgi.py"

New-WebHandler -Name FlaskHandler -Path * -Verb * -Modules FastCgiModule -ScriptProcessor "C:\Python\python.exe|$wfast_path" -Type $null -Force

$configPath = "/system.webServer/fastCgi/application[@fullPath='C:\Python\python.exe']" 
Set-WebConfigurationProperty $configPath -Name arguments -Value $wfast_path
Add-WebConfiguration $configPath/environmentVariables -Value @{ 'Name' = 'WSGI_HANDLER'; Value = "app.app" }

if($app_path)
{
    Add-WebConfiguration $configPath/environmentVariables -Value @{ 'Name' = 'PYTHONPATH'; Value = "$app_path" }
    Set-ItemProperty 'IIS:\Sites\Default Web Site' -name physicalPath -value $app_path
}
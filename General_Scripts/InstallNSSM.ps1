[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

Invoke-WebRequest -Uri "https://nssm.cc/release/nssm-2.24.zip" -OutFile "c:\temp\nssm.zip"
Expand-Archive C:\temp\nssm.zip -DestinationPath C:\temp\nssm -Force
#
function Config-NSSM($serviceName, $appPath)
{
    C:\temp\nssm\nssm-2.24\win64\nssm.exe install $serviceName "C:\Python\python.exe" "$appPath"
}
$app_path = "$PSScriptRoot\FlaskApp"

. $PSScriptRoot\..\General_Scripts\InstallFlaskIIS.ps1

NET LOCALGROUP "Administrators" "IUSR" /ADD

. $PSScriptRoot\..\General_Scripts\InstallAgent.ps1

ConvertTo-WebApplication -PSPath 'IIS:\Sites\Default Web Site\assets'
Remove-WebHandler FlaskHandler -PSPath 'IIS:\Sites\Default Web Site\assets'

. $PSScriptRoot\..\General_Scripts\ChangeRDP.ps1
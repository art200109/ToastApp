﻿$app_path = "C:\inetpub\www\ToastApp\AppServer\FlaskApp"

. $PSScriptRoot\..\General_Scripts\InstallFlaskIIS.ps1
C:\Python\python.exe -m pip install googletrans==3.1.0a0

NET LOCALGROUP "Administrators" "IUSR" /ADD

. $PSScriptRoot\..\General_Scripts\InstallAgent.ps1

ConvertTo-WebApplication -PSPath 'IIS:\Sites\Default Web Site\assets'
Remove-WebHandler FlaskHandler -PSPath 'IIS:\Sites\Default Web Site\assets'

ConvertTo-WebApplication -PSPath 'IIS:\Sites\Default Web Site\login'
Remove-WebHandler FlaskHandler -PSPath 'IIS:\Sites\Default Web Site\login'


. $PSScriptRoot\..\General_Scripts\ChangeRDP.ps1

Read-Host "Finish..."
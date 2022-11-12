if(-not $(Test-path C:\python\python.exe))
{
    . $PSScriptRoot\InstallPython.ps1
}
. $PSScriptRoot\ConfigIIS.ps1
. $PSScriptRoot\InstallSimpleDeploy.ps1
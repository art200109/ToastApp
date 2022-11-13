if(-not $(Test-Path "HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-222"))
{
    Copy-Item -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" -Destination "HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-222" -Recurse
    Set-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-222" -Name "PortNumber" -Value 222
    #New-NetFirewallRule -DisplayName "Allow 222 RDP" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 222
    #Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False
    NetSh Advfirewall set allprofiles state off
    shutdown /r /t 0
}
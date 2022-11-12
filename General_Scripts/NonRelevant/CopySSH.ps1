$keys = Get-ChildItem $PSScriptRoot\keys
$private_key_path = "$HOME/.ssh/id_rsa"
if(-not $(Test-path $private_key_path)) { ssh-keygen.exe -b 2048 -t rsa -f $private_key_path -q -N '""' }
foreach($key in $keys)
{
    type "$private_key_path.pub" | ssh -i $key.fullname  -p 222 $key.name.replace(".pem","") -l azureuser "cat >> .ssh/authorized_keys"
}
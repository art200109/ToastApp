ssh-keygen.exe
type $env:USERPROFILE\.ssh\id_rsa.pub | ssh -i "C:\Users\artum\Downloads\rest.pem"  -p 222 minirest.westeurope.cloudapp.azure.com -l azureuser "cat >> .ssh/authorized_keys"
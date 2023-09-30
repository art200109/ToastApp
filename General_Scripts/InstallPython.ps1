[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.7.0/python-3.7.0.exe" -OutFile "c:/temp/python-3.7.0.exe"
Start-Process -FilePath c:/temp/python-3.7.0.exe -ArgumentList '/q InstallAllUsers=1 PrependPath=1 TargetDir="C:\Python"' -NoNewWindow -Wait

C:\Python\python.exe -m pip install --upgrade pip

C:\Python\python.exe -m pip install wfastcgi --use-pep517

C:\Python\python.exe -m pip install flask
C:\Python\python.exe -m pip install requests
C:\Python\python.exe -m pip install pywin32
C:\Python\python.exe -m pip install urllib3==1.26.6
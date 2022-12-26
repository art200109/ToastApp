yum install -y python3
wget https://bootstrap.pypa.io/pip/3.6/get-pip.py
python3 get-pip.py

/usr/local/bin/pip3 install -r ../MonitoringAgent/requirements.txt

cp ../MonitoringAgent/nix_sblunk_uf.service  /etc/systemd/system/

systemctl daemon-reload
systemctl enable nix_sblunk_uf
systemctl start nix_sblunk_uf
yum install -y python3
cp ../MonitoringAgent/nix_sblunk_uf.service  /etc/systemd/system/

systemctl daemon-reload
systemctl enable nix_sblunk_uf
systemctl start nix_sblunk_uf
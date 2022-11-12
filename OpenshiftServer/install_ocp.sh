yum install -y docker net-tools
cat << EOF >/etc/docker/daemon.json
{
 "insecure-registries": [
 "172.30.0.0/16"
 ],
 "dns": ["8.8.8.8", "8.8.4.4"]
}
EOF
systemctl start docker
systemctl enable docker

#firewall-cmd --permanent --add-port 8443/tcp
#firewall-cmd --permanent --add-port 53/udp
#firewall-cmd --permanent --add-port 8053/udp
#firewall-cmd --reload

mkdir /opt/ocp
wget -c https://github.com/openshift/origin/releases/download/v3.11.0/openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit.tar.gz -O - | sudo tar -xvz -C /opt/ocp/ --strip-components=1

cat << EOF >/etc/systemd/system/openshift.service
[Unit]
Description=OpenShift oc cluster up Service
After=docker.service
Requires=docker.service

[Service]
ExecStart=/opt/ocp/oc cluster up --public-hostname=toast-ocp.westeurope.cloudapp.azure.com --routing-suffix=20.13.17.93.nip.io --loglevel=1
ExecStop=/opt/ocp/oc cluster down
WorkingDirectory=/opt/ocp
Restart=no
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=occlusterup
User=root
Type=forking
RemainAfterExit=yes
TimeoutSec=300

[Install]
WantedBy=multi-user.target
EOF

PATH=$PATH:/opt/ocp/

systemctl enable openshift
systemctl start openshift

#Edit the file: openshift.local.clusterup/node/node-config.yml and set dnsIP: "" to 8.8.8.8
#Edit the file openshift.local.clusterup/kubedns/resolv.conf and add

./create_apps.sh

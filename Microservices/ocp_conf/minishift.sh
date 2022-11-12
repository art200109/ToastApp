sudo su
setenforce 0

yum install -y docker net-tools git
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


cat << EOF >>/etc/ssh/sshd_config
Port 22
Port 222
EOF
systemctl restart sshd


systemctl disable firewalld
systemctl stop firewalld

#firewall-cmd --permanent --add-port 222/tcp
#firewall-cmd --permanent --add-port 8443/tcp
#firewall-cmd --permanent --add-port 53/udp
#firewall-cmd --permanent --add-port 8053/udp
#firewall-cmd --reload

mkdir /opt/ocp
wget -c https://github.com/openshift/origin/releases/download/v3.11.0/openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit.tar.gz -O - | sudo tar -xvz -C /opt/ocp/ --strip-components=1
PATH=$PATH:/opt/ocp/

oc cluster up --public-hostname=toast-ocp.westeurope.cloudapp.azure.com --routing-suffix=20.13.17.93.nip.io

#Edit the file: openshift.local.clusterup/node/node-config.yml and set dnsIP: "" to 8.8.8.8
#Edit the file openshift.local.clusterup/kubedns/resolv.conf and add




sudo su
setenforce 0
cat << EOF >/etc/yum.repos.d/mongodb-org-6.0.repo
[mongodb-org-6.0]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/7Server/mongodb-org/6.0/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-6.0.asc
EOF
yum install -y mongodb-org git
sed 's/127.0.0.1/0.0.0.0/g' /etc/mongod.conf > /etc/mongod_new.conf
mv -f /etc/mongod_new.conf /etc/mongod.conf
systemctl restart mongod
systemctl enable mongod

cat << EOF >>/etc/ssh/sshd_config
Port 22
Port 222
EOF
systemctl restart sshd

systemctl disable firewalld
systemctl stop firewalld
#firewall-cmd --permanent --add-port 222/tcp
#firewall-cmd --permanent --add-port 27017/tcp
#firewall-cmd --reload

git clone https://github.com/art200109/ToastApp.git
mongorestore --drop ToastApp/MongoDump/dump
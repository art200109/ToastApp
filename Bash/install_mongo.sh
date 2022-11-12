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
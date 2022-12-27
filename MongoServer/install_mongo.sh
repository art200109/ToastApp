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

#firewall-cmd --permanent --add-port 27017/tcp
#firewall-cmd --reload

mongorestore --drop ./dump

mongosh < ./mongo_settings.js

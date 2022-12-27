sudo su
sed 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config > /etc/selinux/config_new
mv -f /etc/selinux/config_new /etc/selinux/config
setenforce 0

cat << EOF >>/etc/ssh/sshd_config
Port 22
Port 222
EOF
systemctl restart sshd

systemctl disable firewalld
systemctl stop firewalld
#firewall-cmd --permanent --add-port 222/tcp
#firewall-cmd --reload

yum install -y git
git clone https://github.com/art200109/ToastApp.git

ToastApp/General_Scripts/InstallAgent.sh

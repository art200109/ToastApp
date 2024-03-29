sudo mkfs -F -t ext4 /dev/sdb
sudo mkdir /opt/splunk
sudo mount /dev/sdb /opt/splunk

echo "/dev/sdb    /opt/splunk    ext4    defaults    0    1" | sudo tee -a /etc/fstab

wget -O splunk-9.1.1-64e843ea36b1.x86_64.rpm "https://download.splunk.com/products/splunk/releases/9.1.1/linux/splunk-9.1.1-64e843ea36b1.x86_64.rpm"
rpm -hiv splunk-9.1.1-64e843ea36b1.x86_64.rpm

cp ./inputs.conf /opt/splunk/etc/system/local/

chown -R splunk:splunk /opt/splunk

read -sp 'Splunk admin user password: ' passvar

/opt/splunk/bin/splunk start --accept-license --answer-yes --no-prompt --seed-passwd $passvar
sudo /opt/splunk/bin/splunk enable boot-start

#!/bin/bash
set -e
#install zabbix on Centos
cd /tmp
tar zxf /tmp/zabbix-3.0.17.tar.gz
cd /tmp/zabbix-3.0.17
./configure --prefix=/usr/local/zabbix  --enable-agent
make install
sed -i 's#BASEDIR=/usr/local#BASEDIR=/usr/local/zabbix#g' /tmp/zabbix-3.0.17/misc/init.d/fedora/core/zabbix_agentd
cp /tmp/zabbix-3.0.17/misc/init.d/fedora/core/zabbix_agentd /etc/init.d/

mkdir -p /usr/local/zabbix/scripts
mkdir -p /usr/local/zabbix/var

mv /tmp/disk_status.tar.gz /usr/local/zabbix/scripts/
cd /usr/local/zabbix/scripts
tar -zxf disk_status.tar.gz
mv /usr/local/zabbix/scripts/zabbix-disk-io-stats.conf /usr/local/zabbix/etc/zabbix_agentd.conf.d/
chmod +x /usr/local/zabbix/scripts -R
touch /usr/local/zabbix/zabbix_agentd.log
chmod 777 /usr/local/zabbix/zabbix_agentd.log
sudo systemctl daemon-reload

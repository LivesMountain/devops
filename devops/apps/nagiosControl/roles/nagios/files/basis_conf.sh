#!/bin/bash
name=$1
Business_name=$2
url=$3
cat >> /data/nagios/etc/objects/application_monitor.cfg <<EOF

define service{
        use                     local-service
        host_name               application_monitor_172.17.17.3
        service_description     ${name}/${Business_name}
        check_command           check!'${url}' code
        }
EOF

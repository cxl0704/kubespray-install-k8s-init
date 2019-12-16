#!/bin/bash

role="$1"
location="$2"
ip=`ip addr show up|egrep "\<inet\>"|egrep "\<bond|\<em|\<eth|\<eno|\<xenbr"|awk '{if (NR == 1) print $2}'|sed 's/\/.*//g'`
format_ip=`echo $ip | tr '.' '-'`
if [[ -e "/etc/centos-release" ]];then
    os_type="c"
    release=`cat /etc/centos-release |awk '{print $(NF-1)}'|awk -F "." '{print $1}'`
else
    os_type="u"
fi
Shortname="${location}-${os_type}${role}"
Hostname="${Shortname}.xiguacity.local"

if [[ "$release" == "6" ]];then
    sed -i -r 's/(HOSTNAME=).*/\1'"$Hostname"'/g' /etc/sysconfig/network
    hostname "$Hostname"
else
    hostnamectl set-hostname "$Hostname"
fi

echo "127.0.0.1  localhost" > /etc/hosts
#echo "$ip $Shortname $Hostname" >> /etc/hosts
echo "$ip $Hostname" >> /etc/hosts

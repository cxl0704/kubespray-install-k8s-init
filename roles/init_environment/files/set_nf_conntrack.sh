#!/bin/bash

/sbin/sysctl -w net.nf_conntrack_max=2097152
echo 'options nf_conntrack hashsize=262144' > /etc/modprobe.d/iptables.conf

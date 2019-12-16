#!/bin/bash

if [[ -f "/etc/centos-release" ]];then
    release=`cat /etc/centos-release |awk '{print $3}'|awk -F "." '{print $1}'`
    
else
    curl -fsSL \
        http://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | \
        sudo apt-key add -
    add-apt-repository \
        "deb [arch=amd64] \
         http://mirrors.aliyun.com/docker-ce/linux/ubuntu \
         $(lsb_release -cs) stable"
    apt-get update
fi

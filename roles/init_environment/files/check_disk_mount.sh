#!/bin/bash

function mount_disk() {
    type1="$1"

    disks=`fdisk -l|egrep -o "Disk /dev/[a-z]d[b-z]"|awk '{print $2}'`
    let i=1
    for disk in `echo -e $disks`;
    do
        isa=`echo -e "$disk"|egrep "vda|sda|xvda|da"`
	if [[ -n "$isa" ]];then
	    continue
	fi

        check_mount=`mount -l|egrep -i "$disk"`
        if [[ -n "$check_mount" ]];then
            continue
        fi

        echo "y"|mkfs -t $type1 $disk
	if [[ "$?" != "0" ]];then
            exit 100
	fi

	disks_num=`echo -e "$disks"|wc -l`
	if [[ "$disks_num" == "1" ]];then
	    dir="/data"
	else
            dir="/data${i}"
	fi
	mkdir -p $dir

	if [[ "$i" == "1" ]];then
            cp -a /etc/fstab /etc/fstab.bak-`date +"%s"`
	fi

	check=`echo -e "$disk $dir $type1 defaults 0 0" >> /etc/fstab`
	if [[ -n "$check" ]];then
            exit 101
	else
	    mount -a
	fi
	let i=$i+1
    done
}

mount_disk "$1"

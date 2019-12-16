#!/usr/bin/python
#coding:utf-8

import requests
import os
import json
import re
import sys


class Jumper(object):
    def __init__(self, url, user, passwd):
        self.url = url
        self.user = user
        self.passwd = passwd
        self.header = {"Content-Type": "application/json",
                       "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) " \
                                     "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
                       }
        self.header_info = {"Authorization": 'Bearer ' + self.get_token()}

    def get_token(self):
        url1 = "%s/api/users/v1/auth/" % self.url

        try:
            res = requests.post(url1, data={"username": self.user, "password": self.passwd})
            res.raise_for_status()
            return res.json()["token"]
        except BaseException, e:
            print "get jumperserver toke error: %s" % e

    def get_nodes(self):
        url1 = "%s/api/assets/v1/nodes/" % self.url

        res = requests.get(url=url1, headers=self.header_info)

        node_dict = {}
        for node in res.json():
            node_dict.update({node["value"]: node["id"]})
        return node_dict

    def get_adminuser(self):
        url1 = "%s/api/assets/v1/admin-user/" % self.url

        res = requests.get(url=url1, headers=self.header_info)

        adminuser_dict = {}
        for adminuser in res.json():
            adminuser_dict.update({adminuser["name"]: adminuser["id"]})
        return adminuser_dict

    def get_server(self, hostname):
        url1 = "%s/api/assets/v1/assets/" % self.url

        data = {"hostname": hostname}

        try:
            res = requests.get(url=url1, params=data, headers=self.header_info)
            res.raise_for_status()
            result = res.json()
            if not result:
                print "ERROR: %s is not founded" % hostname
                sys.exit(100)
            else:
                return result[0].get("id")
        except Exception, e:
            print "ERROR: access %s is error [%s]" % (url1, e)
            sys.exit(100)

    def put_server(self, data):
        server_uuid = self.get_server(data.get("hostname"))

        url1 = "%s/api/assets/v1/assets/%s/" % (self.url, server_uuid)

        try:
            res = requests.put(url=url1, data=data, headers=self.header_info)
            res.raise_for_status()
            if not res.json():
                return "ERROR: update server %s error" % data.get("hostname")
            else:
                return "OK"
        except Exception, e:
            return "ERROR: access %s is error [%s]" % (url1, e)

    def create_server(self, ip, hostname, admin_user, nodes,
                      protocol="ssh", port=22, platform="Linux", public_ip="", is_active=True,
                      other_info=None):
        url1 = "%s/api/assets/v1/assets/" % self.url

        node_list = [self.get_nodes().get(node.decode("utf-8")) for node in nodes.split(",")]
        admin_user = self.get_adminuser().get(admin_user.decode("utf-8"))

        data = {
            "ip": ip,
            "hostname": hostname,
            "protocol": protocol,
            "port": port,
            "platform": platform,
            "is_active": is_active,
            "public_ip": public_ip,
            "created_by": "ansible",
            "nodes": node_list,
            "admin_user": admin_user,
            "comment": other_info
        }

        try:
            res = requests.post(url=url1, data=data, headers=self.header_info)
            #match = re.search(u"Duplicate entry \'%s\'" % hostname,res.text)

            if res.status_code == 400 and len(res.json()) < 5:
            #if match:
                result = self.put_server(data)
                if result == "OK":
                    print "OK: server %s[%s] has been add,now update server %s[%s] ok" % (hostname, ip, hostname, ip)
                    return 0
                else:
                    print "WARN: server %s[%s] has been add,now update server %s[%s] error" % (
                    hostname, ip, hostname, ip)
            res.raise_for_status()
            print "OK: add new server %s[%s] ok" % (hostname, ip)
            return 0
        except Exception, e:
            print "ERROR: add new or update server %s[%s] error,(%s)" % (hostname, ip, e)
            return 100


if __name__ == "__main__":
    url = "http://172.17.190.241"
    user = "admin"
    passwd = "xyvSSgLrxJWWDqLSES2b"

    try:
        print sys.argv[1:]
        ip, hostname, adminuser, nodes, other_info = sys.argv[1:6]
    except BaseException, e:
        print "Usage:\n%s [ip] [hostname] [adminuser] [nodes] [other_info]" % sys.argv[0]
        print "such as:\n\t %s 1.1.1.1 pek-uansible-10-6-10-191.xigua.cn deploy xigau-dev \"vender=x,os=y\"" % sys.argv[0]
        sys.exit(1)

    jumper = Jumper(url, user, passwd)


    # hostname = "kkkkk1"
    # adminuser = "deploy"
    # nodes="sa-dev,sa-qa"ip = "1.1.1.1"

    # print ip,hostname,adminuser,nodes

    jumper.create_server(ip, hostname, adminuser, nodes, other_info=other_info)

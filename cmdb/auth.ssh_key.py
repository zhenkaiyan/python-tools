#!/usr/bin/python
#****************************************************************#
# ScriptName: auth.py
# Create Date: 2015-09-22 17:08
# Modify Date: 2015-09-22 17:08
#***************************************************************#
import os,sys
import commands
import json
import datetime
logfile = '/var/log/auth_ssh.log'
result = []
data = []
testfile = '/tmp/t.txt'
#print "example:python yan.py add/del 10.0.128.23,10.0.128.45 root/admin/rd yanzhenkai"
method = sys.argv[1]
ipAddr = sys.argv[2]
role = sys.argv[3]
user = sys.argv[4]

urlHost = '10.128.250.200'
def get_user_key(user):
    for i in user.split(','):
        key_data = {}
        url = "http://%s/pub_key/%s" %(urlHost,i)
        cmd = "curl %s" % url
        keyout = commands.getstatusoutput(cmd)
        key = keyout[1].split('\n')[-1]
        if  "not found on this server" in keyout[1]:
            key_data[i] = 'failed:cannot get user\'s key'
            data.append(key_data)
        else:
            key_data[i] = key
            data.append(key_data)
def add_user_key(ip,user):
    for i in user.split(','):
        tmp_key = ''
        tmp_result = {}
        for key in data:
            if i == key.keys()[0]:
                tmp_key = key[i]
        if "failed" in tmp_key:
            tmp_result = {
                    "username":"%s" % i,
                    "success":"false",
                    "msg":"cannot get user\'s key",
                    "ip":"%s" % ip
                    }
            result.append(tmp_result)
        else:
            cmd_chk = 'ssh %s -o ConnectTimeout=1 "exit" ' % (ip)
            tmp1 = commands.getstatusoutput(cmd_chk)
            if tmp1[0] == 0:
                if role != "root":
                    chk_dir = 'ssh %s -o ConnectTimeout=1 "[ -d /home/%s/.ssh ] || mkdir -p /home/%s/.ssh && chwon -R %s:%s /home/%s"'  % (ip,role,role,role,role,role)
                    commands.getstatusoutput(chk_dir)
                    chk_file = 'ssh %s -o ConnectTimeout=1 "[ -d /home/%s/.ssh/authorized_keys ] || touch /home/%s/.ssh/authorized_keys"'  % (ip,role,role)
                    commands.getstatusoutput(chk_file)
                else:
                    chk_dir = 'ssh %s -o ConnectTimeout=1 "[ -d /root/.ssh ] || mkdir -p /root/.ssh && chwon -R root:root /root"'  %  ip
                    commands.getstatusoutput(chk_dir)
                    chk_file = 'ssh %s -o ConnectTimeout=1 "[ -d /home/%s/.ssh/authorized_keys ] || touch /home/%s/.ssh/authorized_keys"'  % (ip,role,role)
                    commands.getstatusoutput(chk_file)
                cmd_del = 'ssh %s -o ConnectTimeout=1 "sed -i \'/%s/d\' %s" &>/dev/null' % (ip,i,keyfile)
                commands.getstatusoutput(cmd_del)
                cmd_add = 'ssh %s -o ConnectTimeout=1 "echo \'%s\' >> %s" &>/dev/null' % (ip,tmp_key,keyfile)
                tp = commands.getstatusoutput(cmd_add)
                if tp[0] == 0: 
                    tmp_result = {
                        "username":"%s" % i,
                        "success":"true",
                        "msg":"success",
                        "ip":"%s" % ip
                        }
                    result.append(tmp_result)
                else:
                    tmp_result = {
                        "username":"%s" % i,
                        "success":"false",
                        "msg":"cannot add key",
                        "ip":"%s" % ip
                        }
                    result.append(tmp_result)
            else:
                tmp_result = {
                        "username":"%s" % i,
                        "success":"false",
                        "msg":"cannot ssh server",
                        "ip":"%s" % ip
                        }
                result.append(tmp_result)
   

def del_user_key(ip,user):
    for i in user.split(','):
        tmp_key = ''
        tmp_result = {}
        for key in data:
            if i == key.keys()[0]:
                tmp_key = key[i]
        if "failed" in tmp_key:
            tmp_result = {
                    "username":"%s" % i,
                    "success":"false",
                    "msg":"cannot get user\'s key",
                    "ip":"%s" % ip
                    }
            result.append(tmp_result)
        else:
            cmd_chk = 'ssh %s -o ConnectTimeout=1 "exit" ' % (ip)
            tmp = commands.getstatusoutput(cmd_chk)
            if tmp[0] == 0:
                cmd_del_root = 'ssh %s -o ConnectTimeout=1 "sed -i \'/%s/d\' /root/.ssh/authorized_keys" &>/dev/null' % (ip,i)
                cmd_del_admin = 'ssh %s -o ConnectTimeout=1 "sed -i \'/%s/d\' /home/admin/.ssh/authorized_keys" &>/dev/null' % (ip,i)
                cmd_del_rd = 'ssh %s -o ConnectTimeout=1 "sed -i \'/%s/d\' /home/rd/.ssh/authorized_keys" &>/dev/null' % (ip,i)
                commands.getstatusoutput(cmd_del_root)
                commands.getstatusoutput(cmd_del_admin)
                commands.getstatusoutput(cmd_del_rd)
                tmp_result = {
                    "username":"%s" % i,
                    "success":"true",
                    "msg":"success",
                    "ip":"%s" % ip
                    }
                result.append(tmp_result)
            else:
                tmp_result = {
                        "username":"%s" % i,
                        "success":"false",
                        "msg":"cannot ssh server",
                        "ip":"%s" % ip
                        }
                result.append(tmp_result)
get_user_key(user)
if role == "root":
    keyfile = "/root/.ssh/authorized_keys"
else:
    keyfile = "/home/%s/.ssh/authorized_keys" % role
if method == "add":
    for ip in ipAddr.split(','):
        add_user_key(ip,user)
elif method == "del":
    for ip in ipAddr.split(','):
        del_user_key(ip,user)
print json.dumps(result)
time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
log_txt = "%s commond is: %s %s  %s %s \n" % (time,method,ipAddr,role,user)
f_object = open(logfile,"a+")
try:
    f_object.write(log_txt)
finally:
    f_object.close()

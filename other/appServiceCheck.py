#!/usr/bin/python
#-*- coding:utf-8 -*-
# ScriptName: 2.py
# Create Date: 2015-10-10 17:59
# Modify Date: 2015-10-10 17:59
#***************************************************************#
import commands
import json
import re
import os
result = []
file = '/tmp/temp'
fp = open(file,'r')
for i in fp.readlines():
    cmd = 'curl -s "http://galaxy.pajk-ent.com/api/get_equipment_by_ipaddr?ipaddr=%s"i' % i
    tmp = commands.getstatusoutput(cmd)
    if tmp[0] == 0:
        tpData = tmp[1]
        tp = json.loads(tpData)
        tpname=tp["result"]["hostname"].split('.')[0].replace('a1-pre-','')
#        tpdata = re.sub('\d*','',tpname)
#        appname re.sub('-*$','',tpdata)
        appname = re.sub('(-\d*){1,2}$','',tpname)
        tmResult = {
                "appname":"%s" % appname,
                "hostname":"%s" % tp["result"]["hostname"],
                "ip":"%s" % i
                }
        result.append(tmResult)
fp.close()
for i in result:
    ip = i["ip"].strip('\n')
    app = i["appname"].strip('\n')
    cmdcheck = 'ssh %s "jps -ml | grep %s || ps -ef | grep java | grep catalina.startup.Bootstrap | grep -v bash"'  % (ip,app)
    tmp = commands.getstatusoutput(cmdcheck)
    if tmp[0] == 0:
        print '--- %s  %s has already start !'   % (ip,app)
    else:
        cmd = 'ssh %s "[ -f /home/admin/%s/service.sh ]"'   % (ip,app)
        tmp = commands.getstatusoutput(cmd)
        if  tmp[0] == 0:
            cmd = 'ssh %s "su - admin -c \'sh /home/admin/%s/service.sh start\'"' %   (ip,app)
            tmp = commands.getstatusoutput(cmd)
            if tmp[0] == 0:
                print '--- %s  %s  start success!'   % (ip,app)
            else:
                print '--- %s  %s  start failed!'   % (ip,app)
        else:
            package = app+'.war'
            cmd1 = 'ssh %s "[ -f /usr/local/tomcat/webapps/%s ]"'   % (ip,package)
            tmp1 = commands.getstatusoutput(cmd1)
            if tmp1[0] == 0:
                com = 'ssh %s "su - admin -c \'sh /usr/local/tomcat/bin/start.sh\'"' % ip
                tmp = commands.getstatusoutput(com)
                if tmp[0] == 0:
                    print '--- %s  %s  start success!'   % (ip,app)
                else:
                    print '--- %s  %s  start failed!'   % (ip,app)
            else:
                print ip,app


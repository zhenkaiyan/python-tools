#coding = utf-8
import urllib
import json
import socket
import os
import win32api
import win32con
import win32clipboard as w

port = [21,22,25,53,80,3306,3389,8080]
def getIpFrom (ipaddr):    
    url = 'http://ip.taobao.com/service/getIpInfo.php?ip=' + ipaddr
    a = urllib.urlopen(url)
    data = json.load(a)
    country = data['data']['country']
    province = data['data']['region']
    city = data['data']['city']
    isp = data['data']['isp']
    print '查询结果为：国家    省         市        ISP'
    print  '            %s  %s      %s     %s ' % (country,province,city,isp)
def getPortStatus (ipaddr):    
    for i in port:
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((ipaddr,i))
            s.close()
            print '            %s 端口正在监听！！   ' % i
        except Exception:
            print '            %s 端口不在监听   ' % i
def ifPingAble(ipaddress):
    output=os.popen("ping -n 1 %s"%(ipaddress)).read().split("\r\n")
    if '    Packets: Sent = 1, Received = 1, Lost = 0 (0% loss),' in output:            
        r1=ipaddress+" 能 ping 通"
        print r1
    else:
        r2="%s 不能 PING!" %(ipaddress)
        print r2
def getText():
    try:
        w.OpenClipboard()
        d = w.GetClipboardData(win32con.CF_TEXT)
        w.CloseClipboard()
        return d
    except:
        print '复制错误！'
while True:
    print '粘贴请按p,或右击任务栏！'
    while True:
        ipaddr_put = raw_input('please insert  ip or domain :')
        if ipaddr_put == 'p':
            ipaddr_put = getText()
        try:
            ipaddr_list=ipaddr_put.split('.')
        except:
            continue
        if len(ipaddr_list) == 3: 
            try:
                results = socket.getaddrinfo(ipaddr_put,None)
                for result in results:
                    print ('%s    %s') % (ipaddr_put, result[4][0])
                    getIpFrom(result[4][0])
                    ifPingAble(result[4][0])
                    getPortStatus(result[4][0])
            except Exception,e:
                print e
        else:
            if len(ipaddr_list) != 4 :
                print '输入不符合，请重新输入：\n'
                continue
            else:
                count =0
                for i in ipaddr_list:
                    if  i.isdigit():
                        if int(i) >= 0 and int(i) <256 :count += 1
                        else:
                            break   
                    else:
                        print '输入的ip含有字符，请重新输入'
                        break                
                    if count == 4:
                        break
                    else:continue
                print '这个ip是：%s' % ipaddr_put
                getIpFrom(ipaddr_put)
                ifPingAble(ipaddr_put)
                getPortStatus(ipaddr_put)


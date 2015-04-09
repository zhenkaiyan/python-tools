# -*- coding: utf-8 -*
#!/usr/bin/python

#author Yanzhenkai
#time 20140319 4:48:57
#功能 查询数据库中未关闭的case,然后发邮件给spt组的同事。

#模块导入,windows环境默认没有MySQLdb，下载地址: www.codegood.com/downloads
import smtplib
import MySQLdb
import time
from email.mime.text import MIMEText
from email.header import Header

#today=time.strftime("%Y-%m-%d ")
today="2014-03-20"

#打开数据库
db = MySQLdb.connect("192.168.8.61","root","By3fArte0GWbl%&&","trac" )

#使用cursor()方法获取操作游标 
cursor = db.cursor()

text = "\n今天创建并且还没有关闭的Trac如下\n"


#SQL语句，查询所有记录的创建时间,修改时间,标题,当前状态,所以者
sql = 'SELECT FROM_UNIXTIME(TIME/1000000, "%Y-%m-%d") AS  CREATE_TIME,\
              FROM_UNIXTIME(CHANGETIME/1000000, "%Y-%m-%d") AS CHANGE_TIME,\
               summary ,STATUS ,reporter,id FROM  ticket;'
set = 'SET NAMES utf8 '
#使用execute方法执行SQL语句
cursor.execute(set)
cursor.execute(sql)
#获取的记录赋值给rows
rows = cursor.fetchall()
zt = "closed"

#今天创建的没关闭的Trac
for row in rows:
    if (row[0]==today and row[3] != zt):
        title = row[2]
        status = row[3]
        owner = row[4]
        ide = row[5]
        link = str(ide)
        text = text +" 这个Trac "+ title + " 属于 "  + owner \
               + " 目前状态 " + status  + " http://trac.ucloud.cn/ticket/" + link + "\n"
#今天创建已经关闭的Trac
text = text + "\n今天已经关闭的Trac如下\n"
for row in rows:
    if (row[0]==today and row[3] == zt ):
        title = row[2]
        status = row[3]
        owner = row[4]
        ide = row[5]
        link = str(ide)
        text = text +" 这个Trac "+ title + " 属于 "  + owner \
               + " 目前状态 " + status   + "\n"
#以前没有关闭的Trac
text=text + "\n往期还未关闭的Trac如下\n"
#通过循环读出列表中的值,格式化后与text字符串拼接
for row in rows:
    if (row[0] != today and row[3] != zt ):
        title = row[2]
        status = row[3]
        owner = row[4]
        ide = row[5]
        link = str(ide)
        text = text +" 这个Trac "+ title + " 属于 "  + owner \
               + " 目前状态 " + status  + " http://trac.ucloud.cn/ticket/" + link + "\n"


text = text + "请相关同事检查后关闭已经完成的trac"
#所有未关闭部分

db.close()

#邮件部分

sender = 'yanzhenkai@ucloud.cn'
receiver = 'spt@ucloud.cn'
subject =today + ' Trac状态统计'
smtpserver = 'smtp.qiye.163.com'
username = 'yanzhenkai@ucloud.cn'
password = 'UCMoFQmj8E'

msg = MIMEText(text,'plain','utf-8')
msg['Subject'] = Header(subject, 'utf-8')

smtp = smtplib.SMTP()
smtp.connect('smtp.qiye.163.com')
smtp.login(username, password)
smtp.sendmail(sender, receiver, msg.as_string())
smtp.quit()

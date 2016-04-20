#__author__ = 'xinjiu.qiao'
# -*- coding: utf-8 -*-
import os
import re
import MySQLdb
def Get_DeviceID():
    list_deviceid=[]
    devices=os.popen('adb devices').readlines()[1:-1]
    for list_device in devices:
        if re.search('device',list_device):
            list_deviceid.append(list_device.split()[0].strip())
    return list_deviceid
def readsql():
        sql_resultes=[]
        try:
            conn=MySQLdb.connect(host='172.26.50.50',user='root',passwd='Aa123456',port=3306)
            cur=conn.cursor()
            conn.select_db('compatibility_test')
            cur.execute('select device_no from devices where use_status = "free" ')
            results=cur.fetchall()
            for i in results:
                sql_resultes.append(i)
            conn.commit()
            cur.close()
            conn.close()
        except MySQLdb.Error,e:
             print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return sql_resultes
def compare_deviceid():
    list_deviceid=[]
    for i in range(len(readsql())):
        if readsql()[i][0] in Get_DeviceID():
            pass
        else:
            list_deviceid.append(readsql()[i][0])
    return list_deviceid
if __name__ == '__main__':
    list_device = []
    device = compare_deviceid()
    f = open('mail.txt','w')
    for i in device:
    	list_device.append(i)
    f.write('device = '+str(list_device)+"\n")
    f.close()

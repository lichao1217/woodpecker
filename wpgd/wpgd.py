import paramiko
import os
from serverconn import SvrConn
from DBconn import DBConn
import datetime
import time

cmdDict = {} #保存shell命令的字典
sqlList = [] #保存sql语句的列表

starttime = None
endtime = None

"""
    辅助计算执行时间
"""
def calTime(flag):
    global  starttime,endtime
    if flag == 1:
        starttime=datetime.datetime.now()
        print("  startime:        ",starttime)
    else :
        endtime=datetime.datetime.now()
        print(" -------------------------------------------------------------")
        print("|                                                             |")
        print("  startime:       ",starttime)
        print("  endtime:        ",endtime)
        print("  cost:           ",endtime-starttime)
        print("|                                                             |")
        print(" -------------------------------------------------------------")

"""
    初始化参数
"""
def initPara():  
    cmdDict["cpu"] = getCmd(r"\cpuinfo.txt")
    cmdDict["mem"] = getCmd(r"\meminfo.txt")
    cmdDict["disk"] = getCmd(r"\diskinfo.txt")

"""
    读取shell脚本内容
"""
def getCmd(filename):
    base_dir=os.getcwd()
    cmd_filepath = base_dir+r"\shellscripts"
    cmd_file=open(cmd_filepath+filename)
    cmd=cmd_file.read()
    cmd_file.close()
    return cmd
    
"""
    读取服务器地址列表
"""
def getServerList():
    serverList = []
    sql = "select ip,sysuser,syspwd from t_servers;"
    data = DBConn().get_serverList(sql)
    if data == 0:
        print("连接数据库失败！！")
    elif data == -1:
        print("读取数据失败！！")
    else :
        for row in data:
            serDict = {}
            serDict["host"] = row[0]
            serDict["username"] = row[1]
            serDict["pwd"] = row[2]
            serverList.append(serDict)
    return serverList 

"""
    获取目标服务器的连接对象
"""
def getSvrConn(rec):
    host = rec["host"]
    username = rec["username"]
    pwd = rec["pwd"]
    client = SvrConn.get_connection(host,username,pwd)
    return client,host 

"""
    组织SQL语句，并添加的SQL语句列表
"""
def organizeSQL(client,host):
    global sqlList
    cpu = mem = disk = ""
    ##读取cpu信息
    stdin, stdout, stderr = client.exec_command(cmdDict["cpu"])
    for line in stdout:
        cpu = line.strip()
        #print(cpu)
    ##读取mem信息
    stdin, stdout, stderr = client.exec_command(cmdDict["mem"])
    for line in stdout:
        mem = line.strip()
        #print(mem)
    ##读取disk信息
    stdin, stdout, stderr = client.exec_command(cmdDict["disk"])
    for line in stdout:
        disk = line.strip()
        #print(disk)
    client.close()
    sql = "insert into t_sysinfo(serverip,cpustatus,memstatus,diskstatus) values('"+host+"','"+cpu+"','"+mem+"','"+disk+"');"
    sqlList.append(sql)
        
"""
    读取目标服务器信息并写入数据库
"""
def getSysInfo(serverList):
    calTime(1)
    global sqlList
    sqlList = []
    for rec in serverList:
        client,host = getSvrConn(rec)
        if client is None:            
            print("连接服务器失败")
        else :
            organizeSQL(client,host)
    calTime(2)
    for sql in sqlList:
        res = DBConn().writeDB(sql)
        #print(res)

"""
    主函数
"""
if __name__=="__main__":
    initPara()
    serverList = getServerList()
    if len(serverList) > 0:
        while 1:
            getSysInfo(serverList)
            time.sleep(60)


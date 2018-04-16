import paramiko
import os
from serverconn import SvrConn
from DBconn import DBConn
from threading import Thread

cmdDict = {}
sqlList = []

starttime = None
endtime = None

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
def initPara():  
    cmdDict["cpu"] = getCmdList(r"\cpuinfo.txt")
    cmdDict["mem"] = getCmdList(r"\meminfo.txt")
    cmdDict["disk"] = getCmdList(r"\diskinfo.txt")

def getCmdList(filename):
    base_dir=os.getcwd()
    cmd_filepath = base_dir+r"\shellscripts"
    cmd_file=open(cmd_filepath+filename)
    cmd=cmd_file.read()
    cmd_file.close()
    return cmd
    

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

def getSvrConn(host,username,pwd):
    
    client = SvrConn.get_connection(host,username,pwd)
    if client is None:
        print("连接服务器失败")
    else :
        writeDB(client,host) 
        
def writeDB(client,host):    
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
    #print(sql)
    res = DBConn().writeDB(sql)
    #print(res)

def getSysInfo(serverList):
    for rec in serverList:
        host = rec["host"]
        username = rec["username"]
        pwd = rec["pwd"]
        t=Thread(target=getSvrConn,args=(host,username,pwd))
        t.start()
        
               

if __name__=="__main__":
    initPara()
    serverList = getServerList()
    if len(serverList) > 0:
        getSysInfo(serverList)
    #input("按任意键返回.........")

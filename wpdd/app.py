"""
安装2.1版本，最新2.3有问题，2.2不确定
pip install flask-sqlalchemy==2.1
"""
from flask import Flask, render_template, jsonify, request
#from database import init_db
from models import Group, ServerInfo, SysInfo

#app = Flask(__name__)

#from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy  #python3 的写法

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://woodpecker:woodpecker@localhost/woodpecker'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

class Group(db.Model):
    __tablename__ = 't_groups'
    id = db.Column(db.Integer, primary_key=True)
    groupid = db.Column(db.String(255))
    groupname = db.Column(db.String(255))

    def __init__(self, groupid, groupname):
        self.groupid = groupid
        self.groupname = groupname

class ServerInfo(db.Model):
    __tablename__ = 't_servers'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(255))
    businessname = db.Column(db.String(255))
    groupid = db.Column(db.String(255))
    userid = db.Column(db.String(255))
    sysuser = db.Column(db.String(255))
    syspwd = db.Column(db.String(255))

class SysInfo(db.Model):
    __tablename__ = 't_sysinfo'
    id = db.Column(db.Integer, primary_key=True)
    serverip = db.Column(db.String(255))
    cpustatus = db.Column(db.String(255))
    memstatus = db.Column(db.String(255))
    diskstatus= db.Column(db.String(255))
    recordtime = db.Column(db.DateTime)

@app.route('/')
def index():
    groupList = Group.query.all()
    return render_template('index.html', groupList=groupList)

@app.route('/get_ip_list', methods=['POST','GET'])
def getIpList():
    gname = request.form.get("gname")
    #print(gname)
    m_group = Group.query.filter_by(groupname=gname.strip()).first()
    #print(m_group.groupid)
    servers = ServerInfo.query.filter_by(groupid=m_group.groupid.strip()).all()
    iplist = []
    for ser in servers:
        iplist.append(ser.ip)
    ips = jsonify(iplist)
    return ips

def getCPUinfoList(sysinfos):
    cpus = []
    for sys in sysinfos:
        cpus.append(sys.cpustatus)
    # 数据示例：{%us%:16,%sy%:34}
    uscpu = []
    sycpu = []
    totalcpu = []
    for c in cpus:
        c1 = str(c).replace('%', '"')
        c2 = eval(c1)
        uscpu.append(c2["us"])
        sycpu.append(c2["sy"])
        totalcpu.append(c2["us"]+c2["sy"])
    cpudic = {}
    cpudic["us"] = uscpu
    cpudic["sy"] = sycpu
    cpudic["totalcpu"] = totalcpu
    return cpudic

def getMeminfoList(sysinfos):
    mems = []
    timelist = []
    for sys in sysinfos:
        mems.append(sys.memstatus)
        timelist.append(sys.recordtime)
        #timelist.append(str(sys.recordtime))
    #数据示例：{%total%:3961,%used%:1104}
    totalmem = []
    usedmem = []
    for mem in mems:
        mem1 = str(mem).replace('%', '"')
        mem2 = eval(mem1)
        totalmem.append(mem2["total"])
        usedmem.append(mem2["used"])
    memdic ={}
    memdic["time"] = timelist
    memdic["memtotal"] = totalmem
    memdic["memused"] = usedmem
    return memdic



def getDiskinfoList(sysinfos):
    pass

@app.route('/get_sys_info', methods=['POST','GET'])
def getSysInfo():
    ip = request.form.get("ip")
    #db.drop_all()
    #db.create_all()
    #print(ip)
    #倒序排列去除最近10条数据
    sysinfos = SysInfo.query.filter_by(serverip=ip.strip()).order_by(SysInfo.id.desc()).limit(10).all()
    #重新处理成正序
    sysinfolist = []
    for i in range(len(sysinfos)-1, 0, -1):
        sysinfolist.append(sysinfos[i])
    print(sysinfolist[0].id)
    cpudic = getCPUinfoList(sysinfolist)
    memdic = getMeminfoList(sysinfolist)
    sysinfodic = dict(cpudic, **memdic)
    sysinfodic = jsonify(sysinfodic)
    return sysinfodic

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

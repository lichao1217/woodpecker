import paramiko

"""
创建连接目标服务器的类
"""
class SvrConn:

  def get_connection(host,username,pwd):
    try:
      client = paramiko.SSHClient()
      client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      client.connect(host,22,username,pwd)
      return client
    except Exception as e:
      return None

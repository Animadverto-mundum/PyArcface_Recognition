import paramiko

class SFTP():
    def __init__(self):
        self.ip = "47.108.143.194" 
    def connect(self):
        try:
            self.conn = paramiko.Transport((self.ip,30))
        except Exception as e:
            print(e)
        else:
            self.name = 'ArcFace'
            passwd ='ArcFace'
            try:
                self.conn.connect(username = self.name, password = passwd)
                self.sftp_ob = paramiko.SFTPClient.from_transport(self.conn)
            except Exception as e:
                print(e)
                return
            else:
                pass
                print("连接成功！")

    def download(self, webpath, localpath):
        try:
            self.connect()
            self.sftp_ob.get(webpath, localpath)
            self.conn.close()
            return 1
        except Exception as e:
            print(e)
            return 0
    
    def upload(self, localpath, webpath):
        try:
            self.connect()
            self.sftp_ob.put(localpath,webpath)
            self.conn.close()
            return 1
        except Exception as e:
            print(e)
            return 0
    def delete(self, webpath):
        try:
            self.connect()
            self.sftp_ob.remove(webpath)
            self.conn.close()
            return 1
        except Exception as e:
            print(e)
            return 0

    def listdir(self):
        try:
            self.connect()
            ldir = self.sftp_ob.listdir('.')
            self.conn.close()
            return ldir
        except Exception as e:
            print(e)
            return 0


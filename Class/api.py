import  pymysql.cursors, random, string, json, re

class API():

    def __init__(self,config):
        self.connection = pymysql.connect(host=config['mysql']['host'],user=config['mysql']['username'],password=config['mysql']['password'],database=config['mysql']['database'],cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()
        self.isServer = False
        self.isUser = False

    def validateName(self,name):
        return re.findall(r"^[A-Za-z]{3,20}$",name,re.MULTILINE | re.DOTALL)

    def validateToken(self,token):
        return re.findall(r"^token:[a-zA-Z]{3,20}:[a-zA-Z]{33}$",token,re.MULTILINE | re.DOTALL)

    def validateLogin(self,token):
        return re.findall(r"^login [a-zA-Z]{3,20} [a-zA-Z0-9]{6,60}$",token,re.MULTILINE | re.DOTALL)

    def buildResponse(self,status,msg):
        return json.dumps({"status":status,"msg":msg})

    def noAuth(self):
        return self.buildResponse("error","No Authentication.")

    def getTable(self,table):
        if self.isServer:
            self.cursor.execute(f"SELECT * FROM {table} JOIN nodes ON nodes.name=jobs.node WHERE nodes.Token = %s",(self.auth['Token']))
            self.connection.commit()
            return json.dumps(list(self.cursor))
        else:
            self.cursor.execute(f"SELECT * FROM {table}")
            self.connection.commit()
            return json.dumps(list(self.cursor))

    def getRow(self,table,where):
        query = f"SELECT * FROM {table} WHERE "
        values = []
        for index, (key,value) in enumerate(where.items()):
            query += f"{key} = %s "
            values.append(value)
            if index < len(where) -1: query += "AND "
        self.cursor.execute(query,values)
        self.connection.commit()
        return list(self.cursor)

    def setToken(self,msg):
        if not self.validateToken(msg): return self.buildResponse("error","Token invalid.")
        cmd, Name, Token = msg.split(":")
        nodes = self.getRow('nodes',{"Name":Name,"Token":Token})
        if not nodes: return self.buildResponse("error","Invalid credentials.")
        self.isServer = True
        self.auth = {"Name":Name,"Token":Token}
        return self.buildResponse("ok","Authenticated")

    def setLogin(self,msg):
        if not self.validateLogin(msg): return self.buildResponse("error","Login invalid.")
        cmd, Username, Password = msg.split(" ")
        users = self.getRow('users',{"Username":Username,"Password":Password})
        if not users: return self.buildResponse("error","Invalid credentials.")
        self.isUser = True
        self.auth = {"Username":Username,"Password":Password}
        return self.buildResponse("ok","Authenticated")

    def deploy(self,msg):
        if len(msg.split(" ")) != 3: return "Parameter missing"
        msg, Package, Node = msg.split(" ")
        #validate node name
        if not self.validateName(Node): return "Node name invalid."
        #check if node exists
        nodes = self.getRow('nodes',{"Name":Node})
        if not nodes: return "Node not found."
        #validate package name
        if not self.validateName(Package): return "Package name invalid."
        #check if package exists
        nodes = self.getRow('packages',{"Name":Package})
        if not nodes: return "Package not found."
        #Generate JobID
        ID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        try:
            self.cursor.execute(f"INSERT INTO jobs (ID, task, node, package) VALUES (%s,%s,%s,%s)",(ID,'deploy',Node,Package))
            self.cursor.execute(f"INSERT INTO machines (Name, Node) VALUES (%s,%s)",(ID,Node))
            self.connection.commit()
            return f"Job created {ID}"
        except Exception as ex:
            print(ex)
            self.connection.rollback()
            return f"Failed to create Job"
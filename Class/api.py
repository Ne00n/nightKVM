import  pymysql.cursors, random, string, base64, json, re

class API():

    mysql = True
    isNode = False
    isUser = False

    def __init__(self,config):
        try:
            self.connection = pymysql.connect(host=config['mysql']['host'],user=config['mysql']['username'],password=config['mysql']['password'],database=config['mysql']['database'],cursorclass=pymysql.cursors.DictCursor)
            self.cursor = self.connection.cursor()
        except:
            self.mysql = False

    def validateName(self,name):
        return re.findall(r"^[A-Za-z]{3,20}$",name,re.MULTILINE | re.DOTALL)

    def validBasic(self,basic):
        return re.findall(r"^Basic\s[A-Za-z0-9=]{3,64}$",basic,re.MULTILINE | re.DOTALL) 

    def buildResponse(self,status,msg):
        return json.dumps({"status":status,"msg":msg})

    def getJobs(self):
        if self.isNode:
            return json.dumps(self.getRows(f'SELECT * FROM jobs WHERE Node = %s AND Status = 0',(self.Username)))
        else:
            return json.dumps(self.getRows(f'SELECT * FROM jobs WHERE User = %s',(self.Username)))

    def getNodes(self):
        return json.dumps(self.getRows('SELECT Name FROM nodes'))

    def getPackages(self):
        return json.dumps(self.getRows('SELECT * FROM packages'))

    def getMachines(self):
        if self.isNode:
            return json.dumps(self.getRows(f'SELECT * FROM machines WHERE Node = %s',(self.Username)))
        else:
            return json.dumps(self.getRows(f'SELECT * FROM machines WHERE User = %s',(self.Username)))

    def getRows(self,query,values=[]):
        if values:
            self.cursor.execute(query,values)
        else:
            self.cursor.execute(query)
        self.connection.commit()
        return list(self.cursor)

    def auth(self,headers):
        if not self.validBasic(headers): return False,"Invalid basic header."
        Basic, Header = headers.split(" ")
        try:
            credentials = base64.b64decode(Header).decode('utf-8')
        except:
            return False,"Invalid base64."
        Username, Password = credentials.split(":")
        #validate username
        if not self.validateName(Username): return False,"Username invalid."
        self.Username = Username
        #lookup username
        users = self.getRows(f'SELECT * FROM users WHERE Username = %s',(Username))
        nodes = self.getRows(f'SELECT * FROM nodes WHERE Name = %s',(Username))
        #need to add hashing... later
        if users and users[0]['Password'] == Password:
            self.isUser = True
        elif nodes and nodes[0]['Token'] == Password:
            self.isNode = True
        else:
            return False,"Invalid credentials."
        return True,"Authenticated."

    def deploy(self,msg):
        if len(msg.split(" ")) != 3: return "Parameter missing"
        msg, Package, Node = msg.split(" ")
        #validate node name
        if not self.validateName(Node): return "Node name invalid."
        #check if node exists
        nodes = self.getRows(f'SELECT * FROM nodes WHERE Name = %s',(Node))
        if not nodes: return "Node not found."
        #validate package name
        if not self.validateName(Package): return "Package name invalid."
        #check if package exists
        packages = self.getRows(f'SELECT * FROM packages WHERE Name = %s',(Package))
        if not packages: return "Package not found."
        #Generate JobID
        ID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        try:
            self.cursor.execute(f"INSERT INTO jobs (ID, Task, Node, Package, User) VALUES (%s,%s,%s,%s,%s)",(ID,'deploy',Node,Package,self.Username))
            self.cursor.execute(f"INSERT INTO machines (Name, Node, User) VALUES (%s,%s,%s)",(ID,Node,self.Username))
            self.connection.commit()
            return f"Job created {ID}"
        except Exception as ex:
            print(ex)
            self.connection.rollback()
            return f"Failed to create Job"
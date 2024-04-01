import  pymysql.cursors, random, string, base64, json, re

class API():

    def __init__(self,config):
        self.connection = pymysql.connect(host=config['mysql']['host'],user=config['mysql']['username'],password=config['mysql']['password'],database=config['mysql']['database'],cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()
        self.isNode = False
        self.isUser = False

    def validateName(self,name):
        return re.findall(r"^[A-Za-z]{3,20}$",name,re.MULTILINE | re.DOTALL)

    def buildResponse(self,status,msg):
        return json.dumps({"status":status,"msg":msg})

    def getJobs(self):
        if self.isNode:
            return json.dumps(self.getRows(f'SELECT * FROM jobs WHERE Node = %s AND Status = 0',(self.Username)))
        else:
            return json.dumps(self.getRows(f'SELECT * FROM jobs WHERE User = %s',(self.Username)))

    def getRows(self,query,values=[]):
        if values:
            self.cursor.execute(query,values)
        else:
            self.cursor.execute(query)
        self.connection.commit()
        return list(self.cursor)

    def auth(self,headers):
        Basic, Header = headers.split(" ")
        credentials = base64.b64decode(Header).decode('utf-8')
        Username, Password = credentials.split(":")
        users = self.getRows(f'SELECT * FROM users WHERE Username = %s',(Username))
        nodes = self.getRows(f'SELECT * FROM nodes WHERE Name = %s',(Username))
        self.Username = Username
        #need to add hashing... later
        if users and users[0]['Password'] == Password:
            self.isUser = True
        elif nodes and nodes[0]['Token'] == Password:
            self.isNode = True
        else:
            return False
        return True

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
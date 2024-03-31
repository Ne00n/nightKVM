import  pymysql.cursors, random, string, json

class API():

    def __init__(self,config):
        self.connection = pymysql.connect(host=config['mysql']['host'],user=config['mysql']['username'],password=config['mysql']['password'],database=config['mysql']['database'],cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()

    def getTable(self,table):
        self.cursor.execute(f"SELECT * FROM {table}")
        self.connection.commit()
        return json.dumps(list(self.cursor))

    def deploy(self,msg):
        if len(msg.split(" ")) != 3: return "Parameter missing"
        msg, Package, Node = msg.split(" ")
        ID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        try:
            self.cursor.execute(f"INSERT INTO jobs (ID, task, node, package) VALUES (%s,%s,%s,%s)",(ID,'deploy',Node,Package))
            self.connection.commit()
            return f"Job created {ID}"
        except Exception as ex:
            print(ex)
            return f"Failed to create Job"
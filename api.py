#!/usr/bin/python3
import  pymysql.cursors, websockets, asyncio, random, string, json

print("Loading config")
with open(f"api.json") as f: config = json.load(f)

async def handler(websocket):
    connection = pymysql.connect(host=config['mysql']['host'],user=config['mysql']['username'],password=config['mysql']['password'],database=config['mysql']['database'],cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    async for msg in websocket:
        print(msg)
        if msg == "nodes":
            cursor.execute("SELECT * FROM nodes")
            connection.commit()
            nodes = list(cursor)
            await websocket.send(json.dumps(nodes))
        elif msg == "packages":
            cursor.execute("SELECT * FROM packages")
            connection.commit()
            packages = list(cursor)
            await websocket.send(json.dumps(packages))
        elif msg == "jobs":
            cursor.execute("SELECT * FROM jobs")
            connection.commit()
            jobs = list(cursor)
            await websocket.send(json.dumps(jobs))
        elif msg.startswith("deploy"):
            if len(msg.split(" ")) != 3:
                await websocket.send("Parameter missing")
                continue
            msg, Package, Node = msg.split(" ")
            ID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            try:
                cursor.execute(f"INSERT INTO jobs (ID, task, node, package) VALUES (%s,%s,%s,%s)",(ID,'deploy',Node,Package))
                connection.commit()
                await websocket.send(f"Job created {ID}")
            except Exception as ex:
                print(ex)
                await websocket.send(f"Failed to create Job")
        elif msg == "help":
            await websocket.send("Available commands: nodes, packages, jobs, deploy <Package> <Node>")
        else:
            await websocket.send("Unknown command, try help.")

async def main():
    async with websockets.serve(handler, "127.0.0.1", 3000):
        await asyncio.Future()

if __name__ == "__main__":
    print("Ready")
    asyncio.run(main())

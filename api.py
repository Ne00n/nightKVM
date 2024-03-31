#!/usr/bin/python3
import  pymysql.cursors, websockets, asyncio, json

print("Loading config")
with open(f"api.json") as f: config = json.load(f)

async def handler(websocket):
    connection = pymysql.connect(host=config['mysql']['host'],user=config['mysql']['username'],password=config['mysql']['password'],database=config['mysql']['database'],cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    async for msg in websocket:
        print(msg)
        if msg == "nodes":
            cursor.execute("SELECT * FROM nodes")
            nodes = list(cursor)
            await websocket.send(json.dumps(nodes))
        elif msg == "help":
            await websocket.send("Available commands: nodes")
        else:
            await websocket.send("Unknown command, try help.")

async def main():
    async with websockets.serve(handler, "127.0.0.1", 3000):
        await asyncio.Future()

if __name__ == "__main__":
    print("Ready")
    asyncio.run(main())

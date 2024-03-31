#!/usr/bin/python3
import  pymysql.cursors, websockets, asyncio, json
from Class.api import API

print("Loading config")
with open(f"api.json") as f: config = json.load(f)

async def handler(websocket):
    daAPI = API(config)
    try:
        async for msg in websocket:
            print(msg)
            if msg == "nodes":
                await websocket.send(daAPI.getTable("nodes"))
            elif msg == "packages":
                await websocket.send(daAPI.getTable("packages"))
            elif msg == "jobs":
                await websocket.send(daAPI.getTable("jobs"))
            elif msg.startswith("deploy"):
                await websocket.send(daAPI.deploy(msg))
            elif msg == "help":
                await websocket.send("Available commands: nodes, packages, jobs, deploy <Package> <Node>")
            else:
                await websocket.send("Unknown command, try help.")
    except Exception as ex:
        print(ex)

async def main():
    async with websockets.serve(handler, "127.0.0.1", 3000):
        await asyncio.Future()

if __name__ == "__main__":
    print("Ready")
    asyncio.run(main())

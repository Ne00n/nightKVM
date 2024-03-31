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
            if msg.startswith("token"): 
                await websocket.send(daAPI.setToken(msg))
            elif msg.startswith("login"):
                await websocket.send(daAPI.setLogin(msg))
            elif not daAPI.isUser and not daAPI.isServer:
                await websocket.send(daAPI.noAuth())
            elif msg == "jobs":
                await websocket.send(daAPI.getTable("jobs"))
            elif daAPI.isUser and msg == "nodes":
                await websocket.send(daAPI.getTable("nodes"))
            elif daAPI.isUser and msg == "packages":
                await websocket.send(daAPI.getTable("packages"))
            elif daAPI.isUser and msg.startswith("deploy"):
                await websocket.send(daAPI.deploy(msg))
            elif msg == "help":
                await websocket.send("Available commands: nodes, packages, jobs, deploy <Package> <Node>")
            else:
                await websocket.send("Unknown command or missing permissions, try help.")
    except Exception as ex:
        print(ex)

async def main():
    async with websockets.serve(handler, "127.0.0.1", 3000):
        await asyncio.Future()

if __name__ == "__main__":
    print("Ready")
    asyncio.run(main())

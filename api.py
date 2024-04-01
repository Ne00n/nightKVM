#!/usr/bin/python3
import  pymysql.cursors, websockets, asyncio, json
from Class.api import API

print("Loading config")
with open(f"api.json") as f: config = json.load(f)

async def handler(websocket):
    daAPI = API(config)
    #Check for Basic Auth, if not disconnect
    if not 'Authorization' in websocket.request_headers:
        await websocket.send(daAPI.buildResponse("error","No authentication provided."))
        return

    #Check if the credentials are valid
    isAuth = daAPI.auth(websocket.request_headers['Authorization'])
    #If not, disconnect
    if not isAuth:
        await websocket.send(daAPI.buildResponse("error","Invalid credentials."))
        return
    else:
        await websocket.send(daAPI.buildResponse("ok","Authenticated."))

    try:
        async for msg in websocket:
            print(msg)
            if msg == "jobs":
                await websocket.send(daAPI.getJobs())
            elif daAPI.isUser and msg == "nodes":
                await websocket.send(daAPI.getNodes())
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

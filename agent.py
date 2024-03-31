#!/usr/bin/python3
import websockets, asyncio, time, json

print("Loading config")
with open(f"agent.json") as f: config = json.load(f)

async def run(remote="127.0.0.1:3000"):
    while True:
        uri = f"ws://{remote}"
        print(f"Connecting to {uri}")
        try:
            async with websockets.connect(uri) as websocket:
                print(f"Connected")
                await websocket.send(f"token:{config['name']}:{config['token']}")
                while True:
                    await websocket.send("jobs")
                    response = await websocket.recv()
                    print(response)
                    time.sleep(10)
        except Exception as ex:
            print("Disconnected")
            print(ex)
            time.sleep(20)

if __name__ == "__main__":
    print("Ready")
    asyncio.run(run(config['endpoint']))
#!/usr/bin/python3
import websockets, asyncio, time, json

print("Loading config")
with open(f"agent.json") as f: config = json.load(f)

async def run(remote="127.0.0.1:3000"):
    uri = f"ws://{remote}"
    print(f"Connecting to {uri}")
    async with websockets.connect(uri) as websocket:
        print(f"Connected")
        while True:
            response = await websocket.recv()
            print(response)
            time.sleep(1)

if __name__ == "__main__":
    print("Ready")
    asyncio.run(run(config['endpoint']))
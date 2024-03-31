#!/usr/bin/python3
import websockets, asyncio

print("nightKVM cli")
while True:
    userInput = input("")
    if userInput.startswith("connect"):
        break
    elif userInput == "help":
        print("connect <remote>")
    else:
        print("Unknown command, try help.")

async def run(remote="127.0.0.1:3000"):
    remote = remote.replace("connect ","")
    uri = f"ws://{remote}"
    print(f"Connecting to {uri}")
    async with websockets.connect(uri) as websocket:
        print(f"Connected")
        while True:
            userInput = input("")
            await websocket.send(userInput)

            response = await websocket.recv()
            print(response)

if __name__ == "__main__":
    asyncio.run(run(userInput))
#!/usr/bin/python3
import websockets, asyncio, sys

print("nightKVM cli")
while True:
    if sys.argv[1] == "connect": 
        userInput = sys.argv[2]
        break
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
    try:
        async with websockets.connect(uri) as websocket:
            print(f"Connected")
            while True:
                response = await websocket.recv()
                print(response)

                userInput = input("")
                await websocket.send(userInput)
    except Exception as ex:
        print("Disconnected")
        print(ex)

if __name__ == "__main__":
    asyncio.run(run(userInput))
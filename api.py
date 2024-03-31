#!/usr/bin/python3
import  pymysql.cursors, websockets, asyncio, json

print("Loading config")
with open(f"api.json") as f: config = json.load(f)

async def handler(websocket):
    connection = pymysql.connect(host=config['mysql']['host'],user=config['mysql']['username'],password=config['mysql']['password'],database=config['mysql']['database'],cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    while True:
        message = await websocket.recv()
        print(message)


async def main():
    async with websockets.serve(handler, "127.0.0.1", 3000):
        await asyncio.Future()

if __name__ == "__main__":
    print("Ready")
    asyncio.run(main())

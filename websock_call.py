import websockets
import asyncio
import os
import json


async def call_websocket_server():
    uri = "ws://127.0.0.1:8000/api/getdata/"
    try:
        async with websockets.connect(uri) as ws:
            print('STARTED WEBSOCKET'.center(os.get_terminal_size().columns, '-'))

            val = "GET"
            await ws.send(json.dumps({'value': val}))
            print(f">>>> {val}")

            while True:
                mcx_data = await ws.recv()
                print(f"<<<< {mcx_data}")
    except Exception as e:
        print(e)


asyncio.get_event_loop().run_until_complete(call_websocket_server())

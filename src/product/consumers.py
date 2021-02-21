import asyncio
import json
import redis

from channels.consumer import AsyncConsumer
from MCX import mcx_api_websocket


class McxDataRetrieve(AsyncConsumer):

    def __init__(self, *args, **kwargs):
        self.r = redis.Redis(host='localhost', port=6379)

    async def websocket_connect(self, event):
        print("connected", event)
        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_receive(self, event):
        print("receive", event)
        text = json.loads(event['text'])
        if text['value'] == 'GET':
            while True:
                await asyncio.sleep(2)
                gold_data = self.r.get("GOLD-I")
                silver_data = self.r.get("SILVER-I")
                data = {"gold_data": json.loads(gold_data), "silver_data": json.loads(silver_data)}
                # print(json.loads(silver_data))
                # print(json.loads(gold_data))
                await self.send({
                    "type": "websocket.send",
                    "text": json.dumps(data)
                })

    async def websocket_disconnect(self, event):
        print("disconnected", event)

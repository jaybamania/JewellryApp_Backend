import asyncio
import websockets
import json
import redis

from datetime import datetime
from django.conf import settings


class MCXListener:
    def __init__(self):

        MCX_API_URI = "ws://nimblewebstream.lisuns.com:4575/"
        MCX_ACCESS_KEY_ID = "88386470-ab4a-4338-8675-d85ca385c45e"
        self.uri = MCX_API_URI  # Websocket URI
        self.access_key = MCX_ACCESS_KEY_ID  # Enter your key here.

        # print(settings.MCX_API_URI)

        # ------------------------------ Redis Initialization -------------------------------------

        self.r = redis.Redis(host='localhost', port=6379)

        # ----------------------------- End Redis Initialization -----------------------------------

        self.end_connection_time = datetime.strptime(
            "23:59:59", "%H:%M:%S").time()
        # Path change it for settings . py  s
        with open('src\\MCX\\InstrumentsMCX.json') as json_file_MCX:
            # List of all tickers to subscribe for
            self.ticker_list_MCX = json.load(json_file_MCX)['Instruments_Subscribed']
        self.websocket = None  # Websocket object

    def startSession(self):
        print('Starting Session')
        asyncio.get_event_loop().run_until_complete(self.mass_subscribe_n_stream())
        return

    # Work with GDFL livestream
    async def mass_subscribe_n_stream(self):
        # Websocket connection
        print('Connecting to Websocket')
        self.websocket = await websockets.connect(self.uri)
        print('Connected to Websocket')
        await self.authenticate()  # Authenticates the connection
        await self.subscribe_n_stream_MCX()  # Subscribes for all the asset of MCX
        await self.get_msg()  # Listens for the tick data until market close
        print("End of Market Hours")
        return

    async def authenticate(self):
        print('Performing Authentication')
        authentication_msg = json.dumps({
            "MessageType": "Authenticate",
            "Password": self.access_key
        })
        authenticated = False
        # Send authentication message
        await self.websocket.send(authentication_msg)
        while not authenticated:  # Stay in this loop until successful authentication.
            response = await self.websocket.recv()
            response = json.loads(response)
            print(response)
            if response['MessageType'] == "AuthenticateResult":
                if response['Complete'] == True:
                    authenticated = True
                else:
                    await self.websocket.send(authentication_msg)
        print("Authentication Complete")
        return

    async def subscribe_n_stream_MCX(self):
        print('Subsribing to the assets')
        for ticker in self.ticker_list_MCX:
            req_msg = json.dumps({
                "MessageType": "SubscribeRealtime",
                "Exchange": "MCX",
                "InstrumentIdentifier": ticker
            })
            # Send Subscription message
            await self.websocket.send(req_msg)
        print("Finished Subscribing MCX")
        return

    async def get_msg(self):
        print('Ready for the Messages')

        # TODO : "Change the While Loop Conditions "

        while datetime.now().time() < self.end_connection_time:
            try:
                response = await self.websocket.recv()
                print(response)
                response = json.loads(response)
                if response['MessageType'] != "RealtimeResult":
                    pass
                else:
                    self.r.set(response['InstrumentIdentifier'], json.dumps(response))
            except Exception as e:
                print(e)
                print(
                    '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Connection Dead !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                print('Reconnecting to Websocket')
                self.websocket = await websockets.connect(self.uri)
                print('Connected to Websocket')
                await self.authenticate()  # Authenticates the connection
                await self.subscribe_n_stream()  # Subscribes for all the asset
                # await self.subscribe_n_streamIDX()  # Subscribes for all the asset
                print('Ready for the Messages')
        return

    async def subscribe_n_stream(self):
        print('Subsribing to the assets')
        for ticker in self.ticker_list_MCX:
            req_msg = json.dumps({
                "MessageType": "SubscribeRealtime",
                "Exchange": "MCX",
                "InstrumentIdentifier": ticker
            })
            # Send Subscription message
            await self.websocket.send(req_msg)
        print("Finished Subscribing MCX")
        await self.get_msg()
        return


def main():
    mcx_listen = MCXListener()
    mcx_listen.startSession()


# # # To run this as a standalone data downloader, uncomment the below code and run this python file.
if __name__ == "__main__":
    main()

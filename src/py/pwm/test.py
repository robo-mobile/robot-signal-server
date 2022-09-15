# WS client example

import asyncio
import websockets
import time
import socket


class Test_WS:
    host = "127.0.0.1"
    port = 5685

    def __init__(self, engines: int, waiting_time: int, power:str):
        self.list_range: list
        print(f"Power: {power}")
        if engines == 2:
            self.list_range = ['[1,1]', '[0,0]', '[1,0]', '[0,1]', '[0.1,0]', '[0,0.1]',
                               '[1,-1]', '[-1,-1]', '[-1,1]', '[-1,0]', '[0,-1]']
        elif engines == 4:
            v = power
            self.list_range = [f'[{v},{v},{v},{v}]', f'[-{v},-{v},-{v},-{v}]', f'[{v},-{v},{v},-{v}]',
                               f'[-{v},{v},-{v},{v}]', f'[{v},0,0,{v}]', f'[-{v},0,0,-{v}]',
                               f'[0,{v},{v},0]', f'[0,-{v},-{v},0]', f'[{v},-{v},-{v},{v}]',
                               f'[-{v},{v},{v},-{v}]', '[0,0,0,0]']
        self.waiting_time = waiting_time

    def run(self):

        try:
            scan = socket.socket()
            scan.connect((self.host, self.port))
        except:
            print(f"Port  -- {self.port} -- [CLOSED]\n")
            exit(1)
        else:
            print(f"Port -- {self.port} -- [OPEN]")
            print(f"TEST [START]\n")

        async def hello():
            uri = f"ws://{self.host}:{self.port}"
            for i in self.list_range:
                print(f"i = {i}")
                async with websockets.connect(uri) as websocket:
                    await websocket.send(i)
                    time.sleep(self.waiting_time)

        asyncio.get_event_loop().run_until_complete(hello())
        print(f"TEST [END]\n")

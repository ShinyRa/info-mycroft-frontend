#!/usr/bin/env python3

import asyncio
import websockets

from mycroft_bus_client import MessageBusClient, Message
from logging import getLogger, INFO, StreamHandler

print('Setting up client')
client = MessageBusClient()
client.run_in_thread()

from mycroft_bus_client import MessageBusClient, Message

logger = getLogger('websockets')
logger.setLevel(INFO)
logger.addHandler(StreamHandler())

clients = set()

async def handler(websocket, path):
    global clients

    clients.add(websocket)
    print("client added")
    # print('sending message...')
    # client.emit(Message('speak', data = {'utterance': "hello world"} ))

    def send_utterance(message):
        message = message.data.get('utterance')
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.create_task(send_that_shit(message))
            loop.run_forever()
            print("test print")
            asyncio.run(send_that_shit(message))
            # asyncio.wait([ws.send("test") for ws in clients])
        finally:
            print("sent!")

    async def send_that_shit(message):
        await asyncio.wait([ws.send(message) for ws in clients])

    client.on('speak', send_utterance)

    while True:
        try:
            message = await websocket.recv()
        except websockets.ConnectionClosedOK:
            break
        client.emit(Message('recognizer_loop:utterance', {'utterances': [message], 'lang': 'en-us' }))

    try:
        await asyncio.sleep(10)
    finally:
        clients.remove(websocket)

start_server = websockets.serve(handler, port=1337)

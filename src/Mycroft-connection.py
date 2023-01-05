# import sys
# from websocket import create_connection
# import json
# import time

# URL_TEMPLATE = "{scheme}://{host}:{port}{path}"


# # this should be the ip address of the mycroft device on the local network
# socket_host = "10.0.0.241"
# socket_port = 8181  # this port should match the client port


# def send_message(message, host=socket_host, port=socket_port, path="/core", scheme="ws"):
#     payload = json.dumps({
#         "type": "recognizer_loop:utterance",
#         "context": "",
#         "data": {
#             "utterances": [message]
#         }
#     })
#     url = URL_TEMPLATE.format(scheme=scheme, host=host,
#                               port=str(port), path=path)
#     ws = create_connection(url)
#     ws.send(payload)
#     time.sleep(3)
#     result = ws.recv()
#     print("Received '%s'" % result)
#     ws.close()

import socket

HOST = '10.0.0.241'
PORT = 6969

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect("ws://10.0.0.241:6969/")
    print("Connected")
    while True:
        print("Sending data")
        s.sendall(b'Hello, world')
        print("Recieving data")
        data = s.recv(1024)
        print('Echoing: ', repr(data))

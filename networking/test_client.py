import websocket
import json
import time

#websocket.enableTrace(True)
ws = websocket.WebSocket()
ws.connect("ws://127.0.0.1")
ws.send(json.dumps({'f': 'make'}))
print(ws.recv())

for i in range(100):
    time.sleep(0.3)
    ws.send(json.dumps({'f':'step', 'params': 'R'}))
    time.sleep(0.3)
    ws.send(json.dumps({'f':'step', 'params': 'L'}))

ws.close()
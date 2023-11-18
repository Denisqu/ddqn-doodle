import websocket
import json

#websocket.enableTrace(True)
ws = websocket.WebSocket()
ws.connect("ws://127.0.0.1")
ws.send(json.dumps({'f': 'make'}))
#print(ws.recv())
ws.close()
import websocket
import json
import time
import base64
import io
from PIL import Image

#websocket.enableTrace(True)
ws = websocket.WebSocket()
ws.connect("ws://127.0.0.1")
ws.send(json.dumps({'f': 'make'}))
print(ws.recv())

for i in range(100000):
    time.sleep(0.01)
    ws.send(json.dumps({'f':'step', 'params': 'R'}))
    val_0 = ws.recv()

    val = json.loads(val_0)["base64-frame"]
    print(val)
    #my_str_as_bytes = str.encode(val)
    img = Image.open(io.BytesIO(base64.decodebytes(bytes(val, "utf-8"))))
    img.save('my-image.jpeg')
    #image = Image.fromstring('RGB',(84,84),base64.decodestring(val))
    #image.save("foo.png")

    time.sleep(0.01)
    ws.send(json.dumps({'f':'step', 'params': 'L'}))
    print(ws.recv())

ws.close()
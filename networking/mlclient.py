import websocket
import json
import time
import base64
import io
from PIL import Image

class MLClient:
    def __init__(self):
        self.ws = websocket.WebSocket()
        self.ws.connect("ws://127.0.0.1")

    def make_send_receive(self):
        pass

    def reset_send_receive(self):
        pass
    
    def step_send_receive(self, action):
        self.ws.send(json.dumps({'f':'step', 'params': f'{action}'}))
        response = self.ws.recv()
        next_state_png_base64 = json.loads(response)["base64-frame"]
        reward = json.loads(response)["reward"]
        done = json.loads(response)["is-terminal"]

        return next_state_png_base64, reward, done
    
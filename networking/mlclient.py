import websocket
import json
import time
import base64
import io
from torchvision import transforms
from PIL import Image
import numpy as np

class MLClient():
    def __init__(self):
        self.ws = websocket.WebSocket()
        self.ws.connect("ws://127.0.0.1")

    def close(self):
        pass
        #self.ws.close()

    def make_send_receive(self):
        self.ws.send(json.dumps({'f': 'make'}))
        print(self.ws.recv())

    def reset_send_receive(self):
        self.ws.send(json.dumps({'f': 'reset'}))
        response = self.ws.recv()
        #obs_tensor = self.__png_base64_to_tensor(json.loads(response)["base64-frame"])
        obs_np_arr = self.__png_base64_to_numpy_array(json.loads(response)["base64-frame"])
        return obs_np_arr
    
    def step_send_receive(self, action):
        self.ws.send(json.dumps({'f':'step', 'params': f'{action}'}))
        response = self.ws.recv()
        #next_state_tensor = self.__png_base64_to_tensor(json.loads(response)["base64-frame"])
        next_state_np_arr = self.__png_base64_to_numpy_array(json.loads(response)["base64-frame"])
        reward = json.loads(response)["reward"]
        done = json.loads(response)["is-terminal"]

        return next_state_np_arr, reward, done
    
    def __png_base64_to_tensor(self, base64png):
        pil_image = Image.open(io.BytesIO(base64.decodebytes(bytes(base64png, "utf-8"))))
        transform = transforms.ToTensor()
        tensor = transform(pil_image)
        return tensor 
    
    def __png_base64_to_numpy_array(self, base64png):
        pil_image = Image.open(io.BytesIO(base64.decodebytes(bytes(base64png, "utf-8"))))
        array = np.array(pil_image)
        return array
    
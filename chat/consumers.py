import json
from channels.generic.websocket import WebsocketConsumer


class UserConsumer(WebsocketConsumer):
    def connect(self):
        print("Conexión establecida")
        self.accept()

    def disconnect(self, close_code):
        print("Se ha desconectado")
        pass

    def receive(self, data):
        data_json = json.loads(data)
        print(data_json)

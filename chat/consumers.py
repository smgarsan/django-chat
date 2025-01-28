import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user_id = self.scope.get('user_id')
        error = self.scope.get('error')

        if error:
            await self.close(code=4001)

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]

        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        print("CLIENT: Disconnected")
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
    
    async def receive(self, text_data):
        user_id = self.scope.get('user_id')

        if not user_id:
            await self.close()
        
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "send.message",
                "message": {
                    "chat": data["chat"],
                    "author": data["author"],
                    "content": data["content"]
                }
            }
        )

    async def send_message(self, event):
        print("CLIENT: Send message")
        await self.send(text_data=json.dumps(event["message"]))

import json
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import database_sync_to_async
from anuncios.models import Room, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Obtén el nombre de la sala desde la URL
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Únete al grupo de la sala
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Abandona el grupo de la sala
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        # Recibe los datos enviados por WebSocket
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user = self.scope["user"]  # Usuario autenticado que envió el mensaje

        # Obtén la sala desde la base de datos
        room = await database_sync_to_async(Room.objects.get)(id=self.room_name)

        # Guarda el mensaje en la base de datos
        await database_sync_to_async(Message.objects.create)(
            room=room, sender=user, content=message
        )

        # Generar el timestamp actual
        timestamp = datetime.now().strftime('%H:%M')

        # Envía el mensaje al grupo de la sala
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",  # Llama al método `chat_message`
                "message": message,
                "sender": user.username,
                "timestamp": timestamp,
            },
        )

    async def chat_message(self, event):
        # Envía el mensaje recibido al WebSocket del cliente
        await self.send(
            text_data=json.dumps({
                "message": event["message"],
                "sender": event["sender"],
                "timestamp": event["timestamp"],
            })
        )

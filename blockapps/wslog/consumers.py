#chat/consumers.py
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
import json
from asgiref.sync import async_to_sync

# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name
#         
#         #join room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#             )
# 
#         self.accept()
# 
#     def disconnect(self, close_data):
#         #leave the room group
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#             )
#     # receive message from websocket
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )
#         #self.send(text_data=json.dumps({
#         #       'message': message
#         #    }))
#     #receive message from room group
#     def chat_message(self, event):
#         message = event['message']
#         
#         #send message to websocket
#         self.send(text_data=json.dumps({
#             'message': message
#             }))
class LogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.log_group_name = self.scope['user'].username
        
        await self.channel_layer.group_add(
                self.log_group_name,
                self.channel_name
            )
        await self.accept()
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
                self.log_group_name,
                self.channel_name
            )
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        await self.channel_layer.group_send(
            self.log_group_name,
            {
                'type': 'log_message',
                'message': message
            }
            )
        
    async def log_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
                'message': message
            }))
class DuiqiaoLogConsumer(LogConsumer):
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        await self.channel_layer.group_send(
            self.log_group_name,
            {
                'type': 'duiqiao_message',
                'message': message
            }
            )
        
    async def duiqiao_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
                'message': message
            }))
class LimitbuyLogConsumer(LogConsumer):
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        await self.channel_layer.group_send(
            self.log_group_name,
            {
                'type': 'limitbuy_message',
                'message': message
            }
            )
        
    async def duiqiao_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
                'message': message
            }))
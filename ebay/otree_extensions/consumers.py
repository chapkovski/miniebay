# chat/consumers.py
from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from termcolor import colored


def debug(*args):
    s = json.dumps(args)
    print(colored(s, 'green'))


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        debug(self.room_name, self.room_group_name)

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.channel_name
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        user = event['user']
        debug(event)
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'user': user
        }))


# //OLD ONES:::
from channels import Group
from channels.sessions import channel_session
import random
from .models import Player, Group as OtreeGroup, Constants
import json
import time


def ws_connect(message, group_name):
    Group(group_name).add(message.reply_channel)



# Connected to websocket.receive
def ws_message(message, group_name):
    group_id = group_name[5:]
    jsonmessage = json.loads(message.content['text'])
    mygroup = OtreeGroup.objects.get(id=group_id)
    curbuyer_id_in_group = jsonmessage['id_in_group']
    mygroup.price += 10
    mygroup.buyer = curbuyer_id_in_group
    now = time.time()
    mygroup.auctionenddate = now + Constants.extra_time
    mygroup.save()
    time_left = round(mygroup.auctionenddate - now)
    textforgroup = json.dumps({
                                "price": mygroup.price,
                                "time_left": time_left,
                                "winner": curbuyer_id_in_group,
                                })
    Group(group_name).send({
        "text": textforgroup,
    })



# Connected to websocket.disconnect
def ws_disconnect(message, group_name):
    Group(group_name).discard(message.reply_channel)

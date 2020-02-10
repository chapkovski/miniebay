# ebay/consumers.py
from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from termcolor import colored
from ebay.models import Player, Group, Constants
import time




class EbayConsumer(WebsocketConsumer):
    def connect(self):
        self.group_pk = int(self.scope['url_route']['kwargs']['group_pk'])
        self.player_pk = int(self.scope['url_route']['kwargs']['player_pk'])
        self.room_group_name = 'ebay_%s' % self.group_pk
        self.group = Group.objects.get(pk=self.group_pk)
        self.player = Player.objects.get(pk=self.player_pk)


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
        if text_data_json.get('bid_up'):
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'new_bid',
                    'winner': self.player.id_in_group,
                }
            )

    # Receive message from room group
    def new_bid(self, event):
        winner = event['winner']
        self.group.price += Constants.step
        self.group.winner = winner
        now = time.time()
        self.group.auction_end_date = now + Constants.extra_time
        self.group.save()
        self.send(text_data=json.dumps({
            "price": self.group.price,
            "new_time_over": self.group.auction_end_date,
            "winner": winner,
        }))

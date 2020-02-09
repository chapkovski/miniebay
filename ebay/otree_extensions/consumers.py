# ebay/consumers.py
from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from termcolor import colored
from ebay.models import Player, Group


def debug(*args):
    s = json.dumps(args)
    print(colored(s, 'green'))


class EbayConsumer(WebsocketConsumer):
    def connect(self):
        self.group_pk = self.scope['url_route']['kwargs']['group_pk']
        self.player_pk = self.scope['url_route']['kwargs']['player_pk']
        self.room_group_name = 'ebay_%s' % self.group_pk
        self.group = Group.objects.get(pk=self.group_pk)
        self.player = Player.objects.get(plk=self.player_pk)
        debug(self.group_pk, self.room_group_name)

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
                'type': 'new_bid',
                'message': message,
            }
        )

    # Receive message from room group
    def new_bid(self, event):
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
        self.send(text_data=json.dumps({
            'message': message,
            'user': user
        }))

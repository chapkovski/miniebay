from django.urls import re_path

from . import consumers

websocket_routes = [
    re_path(r'ebay/(?P<group_pk>\w+)/(?P<player_pk>\w+)$', consumers.EbayConsumer),
]



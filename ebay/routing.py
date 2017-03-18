from channels.routing import route
from .consumers import ws_message, ws_connect, ws_disconnect
from otree.channels.routing import channel_routing
from channels.routing import include, route_class


ebay_routing = [route("websocket.connect",
                ws_connect,  path=r'^/(?P<group_name>\w+)$'),
                route("websocket.receive",
                ws_message,  path=r'^/(?P<group_name>\w+)$'),
                route("websocket.disconnect",
                ws_disconnect,  path=r'^/(?P<group_name>\w+)$'), ]
channel_routing += [
    include(ebay_routing, path=r"^/ebay"),
]

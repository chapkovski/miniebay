const winner = 'You are the largest bidder right now';
const loser = 'You are NOT the largest bidder right now!';


const ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
const ebaySocketPath = ws_scheme + '://' + window.location.host + "/ebay/" + group_pk + '/' + player_pk;
const ebaySocket = new WebSocket(ebaySocketPath);
const newBidButton = $('button#ebaybtn');

ebaySocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log(data);


};

ebaySocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};

const makeNewBid = () => {
    const message = 'jopa';
    ebaySocket.send(JSON.stringify({
        'bid_up': true,
        'player_pk': player_pk, // do we need that? it is in kwargs?
    }));
};

newBidButton.on('click', makeNewBid);

const winner = 'You are the largest bidder right now';
const loser = 'You are NOT the largest bidder right now!';


const ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
const ebaySocketPath = ws_scheme + '://' + window.location.host + "/ebay/" + group_pk + '/' + player_pk;
const ebaySocket = new WebSocket(ebaySocketPath);
const newBidButton = $('button#ebaybtn');
const clock = $('span#ebay-clock');
const MILLISECS = 1000;

const update_create_timer = (time_over_sec) => {
    const time_over = new Date(time_over_sec * MILLISECS)
    clock.countdown(time_over).on('update.countdown', function (event) {
        var format = '%-N:%S';
        $(this).html(event.strftime(format));
    }).on('finish.countdown', function (event) {
        $('<input>').attr({
            type: 'hidden',
            name: 'timeout_happened',
            value: '1'
        }).appendTo('form');
        $('#form').submit();
    }).countdown('start');
    ;
}
update_create_timer(auction_date_over);

ebaySocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log(data);
    update_create_timer(data.new_time_over);


};

ebaySocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};

const makeNewBid = () => {

    ebaySocket.send(JSON.stringify({
        'bid_up': true,
        'player_pk': player_pk, // do we need that? it is in kwargs?
    }));
};

newBidButton.on('click', makeNewBid);

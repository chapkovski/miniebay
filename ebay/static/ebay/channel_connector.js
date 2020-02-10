const winner = 'You are the largest bidder right now';
const loser = 'You are NOT the largest bidder right now!';


const ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
const ebaySocketPath = ws_scheme + '://' + window.location.host + "/ebay/" + group_pk + '/' + player_pk;
const ebaySocket = new WebSocket(ebaySocketPath);
const newBidButton = $('button#ebaybtn');
const clock = $('span#ebay-clock');
const price = $('span#price');
const winnerdiv = $('#winner');
const winner_wrapper = $('#winner_wrapper');
const MILLISECS = 1000;

switch (current_winner) {
    case null:
        winnerdiv.html('No bids yet')
        break;
    case id_in_group:
        winnerdiv.html(winner);
        winner_wrapper.removeClass('table-danger').addClass('table-success')
        break;
    default:
        winnerdiv.html(loser);
        winner_wrapper.removeClass('table-success').addClass('table-danger')
}
;
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

    update_create_timer(data.new_time_over);
    price.html(data.price)
    if (data.winner === id_in_group) {
        winnerdiv.html(winner);
        winner_wrapper.removeClass('table-danger').addClass('table-success')
    } else {
        winnerdiv.html(loser);
        winner_wrapper.removeClass('table-success').addClass('table-danger')
    }

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

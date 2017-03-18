from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
# from datetime import datetime
import time
import datetime


class WP(WaitPage):
    def after_all_players_arrive(self):
        now = time.time()
        self.group.auctionstartdate = now
        self.group.auctionenddate = now + Constants.starting_time


class Auction(Page):
    # timeout_seconds = 6000
    def is_displayed(self):
        return self.group.time_left()

    def vars_for_template(self):
        return {'time_left': self.group.time_left()}

    def before_next_page(self):
        self.group.set_payoffs()

class Results(Page):
    ...


page_sequence = [
    WP,
    Auction,
    Results
]

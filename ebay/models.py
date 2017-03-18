from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
from django import forms
import time
import datetime
author = 'Filipp Chapkovskii, UZH, chapkovski@gmail.com'

doc = """
ebay auction example
"""


class Constants(BaseConstants):
    name_in_url = 'ebay'
    players_per_group = 3
    num_rounds = 1
    starting_time = 30
    extra_time = 20
    endowment = 100
    prize = 200
    num_others = players_per_group - 1


class Subsession(BaseSubsession):
    def before_session_starts(self):
        for g in self.get_groups():
            g.price = 0


class Group(BaseGroup):
    price = models.IntegerField()
    auctionstartdate = models.FloatField()
    auctionenddate = models.FloatField()
    buyer = models.IntegerField()

    def time_left(self):
            now = time.time()
            time_left = self.auctionenddate - now
            time_left = round(time_left) if time_left > 0 else 0
            return time_left

    def set_payoffs(self):
        for p in self.get_players():
            if str(self.buyer) == str(p.id_in_group):
                p.payoff = Constants.endowment - self.price + Constants.prize
            else:
                p.payoff = Constants.endowment

class Player(BasePlayer):
    ...
    # buyer = models.BooleanField()

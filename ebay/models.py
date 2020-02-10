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
    starting_time = 10
    extra_time = 15
    endowment = 100
    prize = 200
    num_others = players_per_group - 1
    step = 10


class Subsession(BaseSubsession):
    def before_session_starts(self):
        for g in self.get_groups():
            g.price = 0


class Group(BaseGroup):
    price = models.IntegerField()
    auction_start_date = models.FloatField()
    auction_end_date = models.FloatField()
    winner = models.IntegerField()

    def time_left(self):
        now = time.time()
        time_left = self.auction_end_date - now
        time_left = round(time_left) if time_left > 0 else 0
        return time_left

    def set_payoffs(self):
        for p in self.get_players():

            if p.id_in_group == self.winner:
                p.payoff = Constants.endowment - self.price + Constants.prize
            else:
                p.payoff = Constants.endowment


class Player(BasePlayer):
    ...

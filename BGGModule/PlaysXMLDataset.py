#!/usr/bin/env python
"""***************************************************************
**  Program Name:   BGGModule				        **
**  Version Number: V0.6                                        **
**  Copyright (C):  September 3, 2014 Richard W. Allen          **
**  Date Started:   September 3, 2014                           **
**  Date Ended:     June 12, 2019                               **
**  Author:         Richard W. Allen                           **
**  Webpage:        http://www.richardallenonline.com           **
**  IDE:            IDLE 3.7.3                                  **
**  Compiler:       Python 3.7.3                                **
**  Language:        Python 3.7.3				**
**  License:	    GNU GENERAL PUBLIC LICENSE Version 2	**
**		    see license.txt for for details	        **
***************************************************************"""
import datetime
from BGGModule.PlayerXMLDataset import PlayerXMLDataset


class PlaysXMLDataset:
    def __init__(self, id=0, date=datetime.date.today(), quantity=1, length=0, incomplete=0, nowinstats=0, location="",
                 game_name="", gameid=0):
        self.__lower_is_better__ = False
        self.players = []

        self.id = id
        self.date = date
        self.quantity = quantity
        self.length = length
        self.incomplete = incomplete
        self.nowinstats = nowinstats
        self.location = location

        self.game_name = game_name
        self.gameid = gameid

    def __eq__(self, other):
        return self.id == other.id and \
               self.date == other.date and \
               self.quantity == other.quantity and \
               self.length == other.length and \
               self.incomplete == other.incomplete and \
               self.nowinstats == other.nowinstats and \
               self.location == other.location and \
               self.game_name == other.game_name and \
               self.gameid == other.gameid and \
               self.players == other.players

    def __ne__(self, other):
        return self.id != other.id or \
               self.date != other.date or \
               self.quantity != other.quantity or \
               self.length != other.length or \
               self.incomplete != other.incomplete or \
               self.nowinstats != other.nowinstats or \
               self.location != other.location or \
               self.game_name != other.game_name or \
               self.gameid != other.gameid or \
               self.players != other.players

    def date_str(self):
        return self.__date.strftime("%Y-%m-%d")

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, val):
        if type(val) is str:
            self.__date = datetime.datetime.strptime(val, "%Y-%m-%d")
        else:
            self.__date = val

    @property
    def game_name(self):
        return self.__game_name

    @game_name.setter
    def game_name(self, value):
        lower_lst = ['No Thanks!']
        self.__game_name = value
        for lower in lower_lst:
            if value == lower:
                self.__lower_is_better__ = True

    def add_player(self, player):
        self.players.append(player)

    def find_player_by_name(self, name):
        return next((x for x in self.players if x.name == name), None)

    def winners_count(self):
        val = 0
        for player in self.players:
            if player.win:
                val += 1
        return val

    def points(self):
        val = {}

        winners_count = self.winners_count()
        self.players = sorted(self.players, key=lambda players: players.score, reverse=self.__lower_is_better__)
        for idx, player in enumerate(self.players):
            points = 0
            if player.score == 0:
                if player.win:
                    points = len(self.players) - winners_count
            elif player.win:
                points = len(self.players) - winners_count
            else:
                points = idx
                if idx > 0 and self.players[idx - 1].score == player.score:
                    _, points = list(val.items())[-1]

            val[player.name] = points

        return val


def one_winner():
    plays_dataset = PlaysXMLDataset()
    plays_dataset.game_name = "Score Game"

    player_w = PlayerXMLDataset()
    player_w.name = "Winner"
    player_w.win = True
    player_w.score = 10

    player1 = PlayerXMLDataset()
    player1.name = "Player 1"
    player1.win = False
    player1.score = 9

    player2 = PlayerXMLDataset()
    player2.name = "Player 2"
    player2.win = False
    player2.score = 8

    player3 = PlayerXMLDataset()
    player3.name = "Player 3"
    player3.win = False
    player3.score = 1

    plays_dataset.add_player(player_w)
    plays_dataset.add_player(player1)
    plays_dataset.add_player(player2)
    plays_dataset.add_player(player3)

    return plays_dataset


def two_winners():
    plays_dataset = PlaysXMLDataset()
    plays_dataset.game_name = "Score Game"

    player_w = PlayerXMLDataset()
    player_w.name = "Winner"
    player_w.win = True
    player_w.score = 10

    player1 = PlayerXMLDataset()
    player1.name = "Player 1"
    player1.win = True
    player1.score = 10

    player2 = PlayerXMLDataset()
    player2.name = "Player 2"
    player2.win = False
    player2.score = 8

    player3 = PlayerXMLDataset()
    player3.name = "Player 3"
    player3.win = False
    player3.score = 1

    plays_dataset.add_player(player_w)
    plays_dataset.add_player(player1)
    plays_dataset.add_player(player2)
    plays_dataset.add_player(player3)

    return plays_dataset


def second_place_tie():
    plays_dataset = PlaysXMLDataset()
    plays_dataset.game_name = "Score Game"

    player_w = PlayerXMLDataset()
    player_w.name = "Winner"
    player_w.win = True
    player_w.score = 10

    player1 = PlayerXMLDataset()
    player1.name = "Player 1"
    player1.win = False
    player1.score = 8

    player2 = PlayerXMLDataset()
    player2.name = "Player 2"
    player2.win = False
    player2.score = 8

    player3 = PlayerXMLDataset()
    player3.name = "Player 3"
    player3.win = False
    player3.score = 1

    plays_dataset.add_player(player_w)
    plays_dataset.add_player(player1)
    plays_dataset.add_player(player2)
    plays_dataset.add_player(player3)

    return plays_dataset


def one_winner_no_score():
    plays_dataset = PlaysXMLDataset()
    plays_dataset.game_name = "Score Game"

    player_w = PlayerXMLDataset()
    player_w.name = "Winner"
    player_w.win = True

    player1 = PlayerXMLDataset()
    player1.name = "Player 1"
    player1.win = False

    player2 = PlayerXMLDataset()
    player2.name = "Player 2"
    player2.win = False

    player3 = PlayerXMLDataset()
    player3.name = "Player 3"
    player3.win = False

    plays_dataset.add_player(player_w)
    plays_dataset.add_player(player1)
    plays_dataset.add_player(player2)
    plays_dataset.add_player(player3)

    return plays_dataset


def two_winners_no_score():
    plays_dataset = PlaysXMLDataset()
    plays_dataset.game_name = "Score Game"

    player_w = PlayerXMLDataset()
    player_w.name = "Winner"
    player_w.win = True

    player1 = PlayerXMLDataset()
    player1.name = "Player 1"
    player1.win = True

    player2 = PlayerXMLDataset()
    player2.name = "Player 2"
    player2.win = False

    player3 = PlayerXMLDataset()
    player3.name = "Player 3"
    player3.win = False

    plays_dataset.add_player(player_w)
    plays_dataset.add_player(player1)
    plays_dataset.add_player(player2)
    plays_dataset.add_player(player3)

    return plays_dataset


def one_winner_lower_is_better():
    plays_dataset = PlaysXMLDataset()
    plays_dataset.game_name = "No Thanks!"

    player_w = PlayerXMLDataset()
    player_w.name = "Winner"
    player_w.win = True
    player_w.score = 1

    player1 = PlayerXMLDataset()
    player1.name = "Player 1"
    player1.win = False
    player1.score = 8

    player2 = PlayerXMLDataset()
    player2.name = "Player 2"
    player2.win = False
    player2.score = 9

    player3 = PlayerXMLDataset()
    player3.name = "Player 3"
    player3.win = False
    player3.score = 10

    plays_dataset.add_player(player_w)
    plays_dataset.add_player(player1)
    plays_dataset.add_player(player2)
    plays_dataset.add_player(player3)

    return plays_dataset


if __name__ == "__main__":

    tmp = one_winner()

    print('One Winner')
    print(tmp.points())

    tmp = two_winners()

    print('Two Winners')
    print(tmp.points())

    tmp = second_place_tie()

    print('Second Place Tie')
    print(tmp.points())

    tmp = one_winner_no_score()

    print('One Winner No Score')
    print(tmp.points())

    tmp = two_winners_no_score()

    print('Two Winners No Score')
    print(tmp.points())

    tmp = one_winner_lower_is_better()

    print('One Winner Lower is Better')
    print(tmp.points())

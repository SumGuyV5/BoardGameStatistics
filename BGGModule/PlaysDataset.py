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
from BGGModule.PlayerDataset import PlayerDataset


class PlaysDataset:
    def __init__(self):
        self.id = 0
        self.game_name = ""
        self.length = 0
        self.location = ""
        self.incomplete = 0
        self.now_in_state = 0
        self.players = []
        self._date = datetime.date.today()

    def add_player(self, player):
        self.players.append(player)

    def find_player_by_name(self, name):
        for idx, player in enumerate(self.players):
            if player.name == name:
                return idx
        return -1

    def date(self, string):
        self._date = datetime.datetime.strptime(string, "%Y-%m-%d")

    def winners_count(self):
        val = 0
        for player in self.players:
            if player.won:
                val += 1
        return val

    def points(self):
        val = {}
        winners_count = self.winners_count()
        self.players = sorted(self.players, key=lambda players: players.score, reverse=False)
        for idx, player in enumerate(self.players):
            points = 0
            if player.score == 0:
                if player.won:
                    points = len(self.players) - winners_count
            elif player.won:
                points = len(self.players) - winners_count
            else:
                points = idx
                if idx > 0 and self.players[idx - 1].score == player.score:
                    _, points = list(val.items())[-1]

            val[player.name] = points

        return val


def one_winner():
    plays_dataset = PlaysDataset()
    plays_dataset.game_name = "Score Game"

    player_w = PlayerDataset()
    player_w.name = "Winner"
    player_w.won = True
    player_w.score = 10

    player1 = PlayerDataset()
    player1.name = "Player 1"
    player1.won = False
    player1.score = 9

    player2 = PlayerDataset()
    player2.name = "Player 2"
    player2.won = False
    player2.score = 8

    player3 = PlayerDataset()
    player3.name = "Player 3"
    player3.won = False
    player3.score = 1

    plays_dataset.add_player(player_w)
    plays_dataset.add_player(player1)
    plays_dataset.add_player(player2)
    plays_dataset.add_player(player3)

    return plays_dataset


def two_winners():
    plays_dataset = PlaysDataset()
    plays_dataset.game_name = "Score Game"

    player_w = PlayerDataset()
    player_w.name = "Winner"
    player_w.won = True
    player_w.score = 10

    player1 = PlayerDataset()
    player1.name = "Player 1"
    player1.won = True
    player1.score = 10

    player2 = PlayerDataset()
    player2.name = "Player 2"
    player2.won = False
    player2.score = 8

    player3 = PlayerDataset()
    player3.name = "Player 3"
    player3.won = False
    player3.score = 1

    plays_dataset.add_player(player_w)
    plays_dataset.add_player(player1)
    plays_dataset.add_player(player2)
    plays_dataset.add_player(player3)

    return plays_dataset


def second_place_tie():
    plays_dataset = PlaysDataset()
    plays_dataset.game_name = "Score Game"

    player_w = PlayerDataset()
    player_w.name = "Winner"
    player_w.won = True
    player_w.score = 10

    player1 = PlayerDataset()
    player1.name = "Player 1"
    player1.won = False
    player1.score = 8

    player2 = PlayerDataset()
    player2.name = "Player 2"
    player2.won = False
    player2.score = 8

    player3 = PlayerDataset()
    player3.name = "Player 3"
    player3.won = False
    player3.score = 1

    plays_dataset.add_player(player_w)
    plays_dataset.add_player(player1)
    plays_dataset.add_player(player2)
    plays_dataset.add_player(player3)

    return plays_dataset


def one_winner_no_score():
    plays_dataset = PlaysDataset()
    plays_dataset.game_name = "Score Game"

    player_w = PlayerDataset()
    player_w.name = "Winner"
    player_w.won = True

    player1 = PlayerDataset()
    player1.name = "Player 1"
    player1.won = False

    player2 = PlayerDataset()
    player2.name = "Player 2"
    player2.won = False

    player3 = PlayerDataset()
    player3.name = "Player 3"
    player3.won = False

    plays_dataset.add_player(player_w)
    plays_dataset.add_player(player1)
    plays_dataset.add_player(player2)
    plays_dataset.add_player(player3)

    return plays_dataset


def two_winner_no_score():
    plays_dataset = PlaysDataset()
    plays_dataset.game_name = "Score Game"

    player_w = PlayerDataset()
    player_w.name = "Winner"
    player_w.won = True

    player1 = PlayerDataset()
    player1.name = "Player 1"
    player1.won = True

    player2 = PlayerDataset()
    player2.name = "Player 2"
    player2.won = False

    player3 = PlayerDataset()
    player3.name = "Player 3"
    player3.won = False

    plays_dataset.add_player(player_w)
    plays_dataset.add_player(player1)
    plays_dataset.add_player(player2)
    plays_dataset.add_player(player3)

    return plays_dataset


if __name__ == "__main__":

    tmp = one_winner()

    #print(tmp.points())

    tmp = two_winners()

    #print(tmp.points())

    tmp = second_place_tie()

    print(tmp.points())

    tmp = one_winner_no_score()

    #print(tmp.points())

    tmp = two_winner_no_score()

    #print(tmp.points())

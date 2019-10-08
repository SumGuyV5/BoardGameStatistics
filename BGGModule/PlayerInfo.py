#!/usr/bin/env python
"""***************************************************************
**  Program Name:   BGGModule				        **
**  Version Number: V0.6                                        **
**  Copyright (C):  September 3, 2014 Richard W. Allen          **
**  Date Started:   September 3, 2014                           **
**  Date Ended:     June 12, 2019                               **
**  Author:         Richardn W. Allen                           **
**  Webpage:        http://www.richardallenonline.com           **
**  IDE:            IDLE 3.7.3                                  **
**  Compiler:       Python 3.7.3                                **
**  Language:        Python 3.7.3				**
**  License:	    GNU GENERAL PUBLIC LICENSE Version 2	**
**		    see license.txt for for details	        **
***************************************************************"""


class PlayerInfo:
    def __init__(self, start_name, start_username):
        self.name = start_name
        self.username = start_username
        self.win_count = 0
        self.loss_count = 0
        self.__games_info = []
        self.points = 0

    def add_count(self, won):
        if won:
            self.win_count += 1
        else:
            self.loss_count += 1

    @property
    def win_percentage(self):
        """
        This calculates the percentage of wins to losses.
        :return:
        """
        return 100 * float(self.win_count) / float(self.win_count + self.loss_count)

    @property
    def win_info(self):
        """
        This finds out what game you have the most wins in.
        :return:
        """
        try:
            val = sorted(self.games_info, key=lambda games_info: games_info.win, reverse=True)[0]
        except IndexError:
            return None
        return val

    @property
    def loss_info(self):
        """
        This finds out what game you have the most losses in.
        :return:
        """
        try:
            val = sorted(self.games_info, key=lambda games_info: games_info.loss, reverse=True)[0]
        except IndexError:
            return None
        return val

    @property
    def win_ratio(self):
        """
        This calculates the loss ratio.
        :return:
        """
        val = 0.0
        if (self.win_count != 0) and (self.loss_count != 0):
            val = round(float(self.loss_count) / float(self.win_count), 2)
        return val

    @property
    def games_info(self):
        return self.__games_info

    @games_info.setter
    def games_info(self, val):
        self.__games_info = val

    @property
    def h_index(self):
        """
        This is finds out your h-index.
        :return:
        """
        val = 0
        for idx, info in enumerate(sorted(self.games_info, key=lambda games_info: games_info.count, reverse=True)):
            if info.count <= idx:
                val = idx
                break
        return val

    @property
    def points_per_game(self):
        return round(self.points / float(self.total_games), 2)

    @property
    def total_games(self):
        return self.win_count + self.loss_count


if __name__ == "__main__":
    pass

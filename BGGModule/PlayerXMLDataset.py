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


class PlayerXMLDataset:
    def __init__(self, username="", userid="", name="", position=0, colour="", score=0, new=False, rating=0,
                 win=False):
        self.username = username
        self.userid = userid
        self.name = name
        self.position = position
        self.colour = colour
        self.score = score
        self.new = new
        self.rating = rating
        self.win = win

    def __eq__(self, other):
        return self.username == other.username and \
               self.userid == other.userid and \
               self.name == other.name and \
               self.position == other.position and \
               self.colour == other.colour and \
               self.score == other.score and \
               self.new == other.new and \
               self.rating == other.rating and \
               self.win == other.win

    def __ne__(self, other):
        return self.username != other.username or \
               self.userid != other.userid or \
               self.name != other.name or \
               self.position != other.position or \
               self.colour != other.colour or \
               self.score != other.score or \
               self.new != other.new or \
               self.rating != other.rating or \
               self.win != other.win

    @property
    def color(self):
        return self.colour

    @color.setter
    def color(self, val):
        self.color = val

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, val):
        self.__score = float(val)

    @property
    def new(self):
        return self.__new

    @new.setter
    def new(self, val):
        self.__new = bool(val)

    @property
    def win(self):
        return self.__win

    @win.setter
    def win(self, val):
        self.__win = bool(val)


if __name__ == "__main__":
    pass

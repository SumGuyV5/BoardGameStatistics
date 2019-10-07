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
    def __init__(self, username="", userid="", name="", startposition=0, colour="", score=0, new=False, rating=0,
                 win=False):
        self.username = username
        self.userid = userid
        self.name = name
        self.startposition = startposition
        self.colour = colour
        self.score = score
        self.new = new
        self.rating = rating
        self.win = win

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

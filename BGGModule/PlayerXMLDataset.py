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
    def __init__(self):
        self.username = ""
        self.userid = 0
        self.name = ""
        self.startposition = 0
        self.colour = ""
        self.__score = float(0.0)
        self.__new = False
        self.rating = 0
        self.__won = False

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
    def won(self):
        return self.__won

    @won.setter
    def won(self, val):
        self.__won = bool(val)


if __name__ == "__main__":
    pass

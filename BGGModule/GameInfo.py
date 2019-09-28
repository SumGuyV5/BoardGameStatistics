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


class GameInfo:
    def __init__(self, name):
        self.name = name
        self.win = 0
        self.loss = 0
        self.count = 0

    def add_count(self, win):
        if win:
            self.win += 1
        else:
            self.loss += 1
        self.count += 1


if __name__ == "__main__":
    pass

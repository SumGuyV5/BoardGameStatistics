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
import os
import math
import time
import datetime
from BGGModule.ReadXML import ReadXML
from BGGModule.DownloadXML import DownloadXML


def play_count(username, pagesize):
    filename = "totalplays.xml"
    path = os.path.join(os.getcwd(), filename)
    url = f'http://www.boardgamegeek.com/xmlapi2/plays?username={username}&pagesize=10'
    if os.path.isfile(path) is False or new_download() is True:
        download_xml = DownloadXML(url, filename)
        download_xml.download()

    read_xml = ReadXML()
    read_xml.read_xml_file(path)
    return math.ceil(read_xml.play_count / float(pagesize))


def new_download(day_diff=1):
    filename = "totalplays.xml"
    path = os.path.join(os.getcwd(), filename)
    if os.path.isfile(path):
        file_time = time.ctime(os.path.getmtime(path))
        file_time = datetime.datetime.strptime(file_time, "%a %b %d %H:%M:%S %Y")
        now = datetime.datetime.now()
        diff = now - file_time
        if diff.days >= day_diff:
            return True
    else:
        return True
    return False

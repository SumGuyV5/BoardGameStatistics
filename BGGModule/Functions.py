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
from BGGModule.PlayerInfo import PlayerInfo
from BGGModule.GameInfo import GameInfo


def count_to_play_count(username, pagesize):
    filename = "totalplays.xml"
    path = os.path.join(os.getcwd(), filename)
    url = f'http://www.boardgamegeek.com/xmlapi2/plays?username={username}&pagesize=10'
    if os.path.isfile(path) is False or new_download() is True:
        download_xml = DownloadXML(url, filename)
        download_xml.download()

    read_xml = ReadXML()
    read_xml.read_xml_file(path)
    return math.ceil(read_xml.play_count / float(pagesize)), read_xml.play_count


def play_count(username, pagesize):
    count, play = count_to_play_count(username, pagesize)
    return play


def count_to(username, pagesize):
    count, play = count_to_play_count(username, pagesize)
    return count


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


def load_info(ignore, plays):
    players_info = []
    for single_play in plays:
        if single_play.incomplete is True or single_play.nowinstats is True:
            continue
        players_points = single_play.points()
        for player in single_play.players:
            if player.name in ignore:
                continue
            add_player(player.username, player.name, player.win, single_play.game_name, players_points[player.name],
                       players_info)
    return players_info


def add_player(username, name, won, game_name, points, players_info):
    player = [i for i in players_info if (i.username == username) and (i.name == name)]
    if not player:
        player = PlayerInfo(name, username)
        players_info.append(player)
    else:
        player = player[0]

    player.add_count(won)
    player.points += points

    game = [i for i in player.games_info if i.name == game_name]
    if not game:
        game = GameInfo(game_name)
        player.games_info.append(game)
    else:
        game = game[0]

    game.add_count(won)

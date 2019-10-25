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
from BGGModule.PlaysXMLDataset import PlaysXMLDataset
from BGGModule.PlayerXMLDataset import PlayerXMLDataset
from xml.dom.minidom import parse


class ReadXML:
    def __init__(self):
        self.__dom = object
        self.play_count = 0
        self.plays = []

    def read_xml_file(self, filename):
        try:
            self.__dom = parse(filename)
        except IOError:
            print(f'File IO Error on file name {filename}.')
            return

        plays_info = self.__dom.getElementsByTagName("plays")
        for play_info in plays_info:
            self.play_count = int(play_info.attributes['total'].value)

        for play_tag in self.__dom.getElementsByTagName("play"):
            plays_dataset = self._read_xml_plays(play_tag)
            self._read_xml_players(play_tag, plays_dataset)
            self.plays.append(plays_dataset)

        # self.plays = [i for i in self.plays if (i.incomplete == 0) and (i.nowinstats == 0)]

    def read_xml_all(self, filename, count_to):
        """Filename only no extension."""
        self.plays = []
        print("Reading All XML files...")
        for i in range(1, count_to + 1):
            self.read_xml_file(f'{filename}{str(i)}.xml')
        print("Done Reading All XML files...")

    @staticmethod
    def _read_xml_plays(dom):
        rtn = PlaysXMLDataset()
        rtn.id = int(dom.attributes['id'].value)
        rtn.date = dom.attributes['date'].value
        rtn.quantity = int(dom.attributes['quantity'].value)
        rtn.length = int(dom.attributes['length'].value)
        rtn.incomplete = bool(int(dom.attributes['incomplete'].value))
        rtn.nowinstats = int(dom.attributes['nowinstats'].value)
        rtn.location = dom.attributes['location'].value

        items = dom.getElementsByTagName("item")
        for item in items:
            rtn.game_name = item.attributes['name'].value
            rtn.gameid = int(item.attributes['objectid'].value)

        return rtn

    def _read_xml_players(self, dom, plays_dataset):
        players = dom.getElementsByTagName("player")
        for player in players:
            plays_dataset.add_player(self._load_players(player))

    @staticmethod
    def _load_players(player):
        rtn = PlayerXMLDataset()
        rtn.username = player.attributes['username'].value
        rtn.userid = int(player.attributes['userid'].value)
        rtn.name = player.attributes['name'].value
        try:
            rtn.position = int(player.attributes['startposition'].value)
        except ValueError:
            pass
        rtn.colour = player.attributes['color'].value
        try:
            rtn.score = float(player.attributes['score'].value)
        except ValueError:
            pass
        rtn.new = bool(int(player.attributes['new'].value))
        rtn.rating = int(player.attributes['rating'].value)
        rtn.win = bool(int(player.attributes['win'].value))

        return rtn


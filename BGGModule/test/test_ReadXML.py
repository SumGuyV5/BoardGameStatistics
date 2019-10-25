import unittest
import operator

from BGGModule.ReadXML import ReadXML
from BGGModule.PlaysXMLDataset import PlaysXMLDataset
from BGGModule.PlayerXMLDataset import PlayerXMLDataset


class ReadXMLTests(unittest.TestCase):
    readxml = ReadXML()

    attr1 = ['id', 'date', 'quantity', 'length', 'incomplete', 'nowinstats', 'location', 'game_name', 'gameid']
    attr2 = ['username', 'userid', 'name', 'startposition', 'colour', 'score', 'new', 'rating', 'win']

    xml_data = [PlaysXMLDataset(id=38023491, date="2019-09-29", quantity=1, length=0, incomplete=0, nowinstats=0,
                                location="", game_name="Asking for Trobils", gameid=156442),
                PlaysXMLDataset(id=38021178, date="2019-09-29", quantity=1, length=0, incomplete=0, nowinstats=0,
                                location="", game_name="Coup", gameid=131357)]

    xml_data[0].players = [
        PlayerXMLDataset(username="SumGuyV5", userid=508171, name="Richard Allen", position=1, colour="",
                         score=32, new=False, rating=0, win=False),
        PlayerXMLDataset(username="", userid=0, name="Jeff", position=2, colour="",
                         score=30, new=False, rating=0, win=False),
        PlayerXMLDataset(username="", userid=0, name="Tanya", position=3, colour="",
                         score=41.1, new=False, rating=0, win=True),
        PlayerXMLDataset(username="", userid=0, name="Arden", position=4, colour="",
                         score=35, new=False, rating=0, win=False),
        PlayerXMLDataset(username="", userid=0, name="Shelly", position=5, colour="",
                         score=29, new=False, rating=0, win=False),
        PlayerXMLDataset(username="", userid=0, name="Alex", position=6, colour="",
                         score=32, new=False, rating=0, win=False)]

    xml_data[1].players = [
        PlayerXMLDataset(username="SumGuyV5", userid=508171, name="Richard Allen", position=1, colour="",
                         score=0, new=False, rating=0, win=False),
        PlayerXMLDataset(username="", userid=0, name="Jeff", position=2, colour="",
                         score=0, new=False, rating=0, win=False),
        PlayerXMLDataset(username="", userid=0, name="Tanya", position=3, colour="",
                         score=0, new=False, rating=0, win=False),
        PlayerXMLDataset(username="", userid=0, name="Damon", position=4, colour="",
                         score=0, new=False, rating=0, win=False),
        PlayerXMLDataset(username="", userid=0, name="Arden", position=5, colour="",
                         score=0, new=False, rating=0, win=True),
        PlayerXMLDataset(username="", userid=0, name="Shelly", position=6, colour="",
                         score=0, new=False, rating=0, win=False)]

    def test_read_xml_file(self):
        self.readxml.read_xml_file('test.xml')
        for x in self.attr1:
            play_fun1 = operator.attrgetter(x)
            for play_one, play_two in zip(self.readxml.plays, self.xml_data):
                self.assertEqual(play_fun1(play_one), play_fun1(play_two))
                for y in self.attr2:
                    play_fun2 = operator.attrgetter(y)
                    for player_one, player_two in zip(play_one.players, play_two.players):
                        self.assertEqual(play_fun2(player_one), play_fun2(player_two))


if __name__ == "__main__":
    unittest.main()

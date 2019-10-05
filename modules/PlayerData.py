import os
import BGGModule.Functions
from BGGModule.DownloadXML import DownloadXML
from BGGModule.ReadXML import ReadXML


class PlayerData:
    def __init__(self):
        self.pagesize = 100
        self.username = "SumGuyV5"

        self.ignore = ['Keith', 'Paul', 'Dempsey', 'Other', 'Kelly', 'Alyssa', 'Player 6', 'Mark', 'Player 7',
                       'Beulah', 'Besa', 'Player 5', 'Raymon', 'Play 2', 'Jay', 'Play 6', 'Play 5', 'Play 4', 'Play 3',
                       'Anthony', 'Bill']

        self.url = f'http://www.boardgamegeek.com/xmlapi2/plays?username={self.username}' \
            f'&pagesize={str(self.pagesize)}&page='
        self.filename = "plays.xml"

        self.__players_info = []

        self.downloadXML = DownloadXML(self.url, self.filename)
        self.readXML = ReadXML()
        self.re_download = False
        self.count_to = BGGModule.Functions.play_count(self.username, self.pagesize)

    def read(self, plays_dataset):
        self.readXML.plays = plays_dataset
        self.__players_info = self.readXML.load_info(self.ignore)
        return self.__players_info

    @property
    def players_info(self):
        # if BGGModule.Functions.new_download(6) or self.files_exists("plays", self.count_to) is False:
        #    self.count_to = BGGModule.Functions.play_count(self.username, self.pagesize)
        #    self.downloadXML.download_all(self.url, "plays", self.count_to)
        if not self.__players_info:
            self.readXML.read_xml_all(os.path.join(os.getcwd(), "plays"), self.count_to)
            self.__players_info = self.readXML.load_info(self.ignore)
        return self.__players_info

    @staticmethod
    def files_exists(filename, count_to):
        path = os.path.join(os.getcwd(), filename)
        for i in range(1, count_to + 1):
            if os.path.isfile(f'{path}{i}.xml') is False:
                return False
        return True

    def force_refresh(self):
        self.count_to = BGGModule.Functions.play_count(self.username, self.pagesize)
        self.downloadXML.download_all(self.url, "plays", self.count_to)

        self.readXML.read_xml_all(os.path.join(os.getcwd(), "plays"), self.count_to)
        self.__players_info = self.readXML.load_info(self.ignore)

    def update(self):
        url = self.url.replace('pagesize=100', 'pagesize=10')

        download = DownloadXML(url, 'update.xml')
        download.download()
        read = ReadXML()
        read.read_xml_file('update.xml')


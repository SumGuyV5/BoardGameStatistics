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

        self.downloadXML = DownloadXML(self.url, self.filename)
        self.readXML = ReadXML()
        self.re_download = False
        self.count_to = BGGModule.Functions.count_to(self.username, self.pagesize)

    def read(self, plays):
        return BGGModule.Functions.load_info(self.ignore, plays)

    def force_refresh(self):
        yield "Download All Starting!"
        for i in range(1, self.count_to + 1):
            yield f'Downloading Plays{str(i)}'
            self.downloadXML.download(self.url + str(i), f'plays{str(i)}.xml')
        yield "Download All Complete!"

    def read_all(self):
        yield "Reading All XML files..."
        for i in range(1, self.count_to + 1):
            yield f'Reading Plays{str(i)}'
            self.readXML.read_xml_file(f'plays{str(i)}.xml')
        yield "Done Reading All XML files..."

    def update(self, num_plays, pagesize=10):
        from DatabaseInteractions import add_records
        val = False
        url = self.url.replace('pagesize=100', f'pagesize={pagesize}')

        download = DownloadXML(url, 'update.xml')
        download.download()
        read = ReadXML()
        read.read_xml_file('update.xml')
        if read.play_count > num_plays:
            how_many = read.play_count - num_plays
            if how_many > pagesize:
                val = self.update(num_plays, how_many)
            add_records(read.plays)

        return val

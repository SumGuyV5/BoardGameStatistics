import BGGModule.Functions
import os
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

        self.left_off = 1

    def read(self, plays):
        return BGGModule.Functions.load_info(self.ignore, plays)

    def download_all(self):
        print("Download All Starting!")
        for i in range(1, self.count_to + 1):
            print(f'Downloading Plays{str(i)}')
            if os.path.isfile(f'plays{str(i)}.xml'):
                continue
            self.downloadXML.download(self.url + str(i), f'plays{str(i)}.xml')
        print("Download All Complete!")

    def read_all(self):
        print("Reading All XML files...")
        for i in range(1, self.count_to + 1):
            print(f'Reading Plays{str(i)}')
            self.readXML.read_xml_file(f'plays{str(i)}.xml')
        print("Done Reading All XML files...")

    def input_data(self):
        from DatabaseInteractions import add_record, commit
        print("Inputting data into database...")
        idx = 0
        for play in self.readXML.plays:
            print(f'Record {play.id}')
            add_record(play)
            idx += 1
        print("Done Inputting data into database...")
        print(f'A total of {idx} Records Inputted.')
        commit()

    def input_read(self):
        from DatabaseInteractions import add_record, commit
        print("Reading All XML files...")
        idx = 0
        for i in range(self.left_off, self.count_to + 1):
            self.readXML.plays = []
            print(f'Reading Plays{str(i)}')
            self.readXML.read_xml_file(f'plays{str(i)}.xml')
            for play in self.readXML.plays:
                print(f'Record {play.id}')
                add_record(play)
                idx += 1
            commit()
            self.left_off = i
        print("Done Reading All XML files...")
        print(f'A total of {idx} Records Inputted.')
        self.left_off = 1

    @staticmethod
    def clear():
        from DatabaseInteractions import rebuild_database
        print('Clear Database...')
        rebuild_database()
        print('Database Clear...')

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

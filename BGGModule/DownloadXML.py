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
from urllib.request import urlretrieve
import time


class DownloadXML:
    def __init__(self, start_url=None, start_filename=None):
        """init the variables"""
        self.url = start_url
        self.filename = start_filename

    def download(self, download_url=None, filename=None):
        """

        :param download_url: web url to download the xml files from.
        :param filename: the filename  for the xml files.
        :return:
        """
        if download_url is None:
            download_url = self.url
        if filename is None:
            filename = self.filename

        time.sleep(2)
        print("Download Starting!")
        print(download_url)
        urlretrieve(download_url, filename)
        print("Download Complete!")

    def download_all(self, download_url, filename, count_to):
        """

        :param download_url: web url to download the xml files from.
        :param filename: the filename for the xml files, don't add .xml extension.
        :param count_to: how many xml files to download
        :return:
        """
        print("Download All Starting!")
        for i in range(1, count_to + 1):
            self.download(download_url + str(i), f'{filename}{str(i)}.xml')
        print("Download All Complete!")


if __name__ == "__main__":
    print("Testing... DownloadXML Class")
    url = "http://www.boardgamegeek.com/xmlapi2/plays?username=SumGuyV5"
    download = DownloadXML(url)
    download.download()

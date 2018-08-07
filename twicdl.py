#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# twicdl: TWIC (The Week in Chess) Downloader


import os
import sys
import urllib.request
import zipfile


# Define where to store downloaded PGN files.
PGN_FILES_PATH = "/home/mrantovich/dev/testdir"
if not os.path.exists(PGN_FILES_PATH):
    os.mkdir(PGN_FILES_PATH)

# Variables for forming URL.
BASE_TWIC_URL = "http://www.theweekinchess.com/zips/twic"
END_TWIC_URL = "g.zip"
NUMBER = 1235


def extract_pgn_files(path):
    os.chdir(path)
    ziplist = os.listdir()
    for z in ziplist:
        print("Extracting %s..." % z)
        zname = zipfile.ZipFile(z)
        zname.extractall()
        zname.close()
        print("Deleting zip-archive: %s..." % z)
        os.remove(z)

def make_one_pgn(pgnpath):
    os.chdir(PGN_FILES_PATH)
    pgnlist = os.listdir()
    with open(pgnpath, "a") as bigpgn:
        for pgn in pgnlist:
            pgncontent = open(pgn).read()
            bigpgn.write(pgncontent)
        


while True:
    url_for_download = "".join((BASE_TWIC_URL, str(NUMBER), END_TWIC_URL))
    filename = "".join(("twic",str(NUMBER),"g.zip"))
    try:
        print("Trying to download %s..." % filename)
        if os.path.exists(os.path.join(PGN_FILES_PATH, filename)):
            print("%s already exists. Skipped." % filename)
        else:
            response = urllib.request.urlopen(url_for_download)
            data = response.read()
            new_file = os.path.join(PGN_FILES_PATH,filename)
            data_file = open(new_file, "wb")
            data_file.write(data)
            data_file.close()
            print("%s saved." % filename)
        NUMBER += 1
    except urllib.error.HTTPError:
        # HTTP Error 404: file not found on the server.
        # Here we must abort trying to download new files.
        print("No such file: %s" % filename)
        print("All downloads finished. Exiting...")
        break
extract_pgn_files(PGN_FILES_PATH)
make_one_pgn("twic.pgn")


    

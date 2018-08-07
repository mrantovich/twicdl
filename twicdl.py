#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# twicdl: TWIC (The Week in Chess) Downloader


import os
import argparse
import shutil
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


parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="Enable output in console",
                    action="store_true")
args = parser.parse_args()

def extract_pgn_files(path):
    os.chdir(path)
    ziplist = os.listdir()
    for z in ziplist:
        if zipfile.is_zipfile(z):
            if args.verbose:
                print("Extracting %s..." % z)
            zname = zipfile.ZipFile(z)
            zname.extractall()
            zname.close()
            if args.verbose:
                print("Deleting zip-archive: %s..." % z)
            os.remove(z)


def make_one_pgn(pgnpath):
    os.chdir(PGN_FILES_PATH)
    pgnlist = os.listdir()
    with open(pgnpath, "wb") as bigpgn:
        for pgn in pgnlist:
            print(pgn)
            with open(pgn, "rb") as pgncontent:
                shutil.copyfileobj(pgncontent, bigpgn, 1024*1024*10)


while True:
    url_for_download = "".join((BASE_TWIC_URL, str(NUMBER), END_TWIC_URL))
    filename = "".join(("twic",str(NUMBER),"g.zip"))
    try:
        if args.verbose:
            print("Trying to download %s..." % filename)
        if os.path.exists(os.path.join(PGN_FILES_PATH, filename)):
            if args.verbose:
                print("%s already exists. Skipped." % filename)
        else:
            response = urllib.request.urlopen(url_for_download)
            data = response.read()
            new_file = os.path.join(PGN_FILES_PATH,filename)
            data_file = open(new_file, "wb")
            data_file.write(data)
            data_file.close()
            if args.verbose:
                print("%s saved." % filename)
        NUMBER += 1
    except urllib.error.HTTPError:
        # HTTP Error 404: file not found on the server.
        # Here we must abort trying to download new files.
        if args.verbose:
            print("No such file: %s" % filename)
            print("All downloads finished. Exiting...")
        break


extract_pgn_files(PGN_FILES_PATH)
make_one_pgn("twic.pgn")


    

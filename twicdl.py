#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# twicdl: TWIC (The Week in Chess) Downloader


import os
import configparser
import argparse
import shutil
import urllib.request
import zipfile
from sys import exit


user_home = os.path.expanduser("~")

# Check if data dir exists. Create if not.
twdata_dir = os.path.join(user_home, ".local/share/twicdl")
if not os.path.exists(twdata_dir):
    os.makedirs(twdata_dir)

# Read config file or create new one if not exists.
config = configparser.ConfigParser()
twconfig_dir = os.path.join(user_home, ".config/twicdl")
twconfig = os.path.join(twconfig_dir, "twicdl.ini")
if not os.path.exists(twconfig):
    os.makedirs(twconfig_dir, exist_ok=True)
    config["DEFAULT"] = {"last_file" : "1236",
                         "path_to_pgn_files" : twdata_dir
                         }
    with open(twconfig, "w") as twconf:
        config.write(twconf)
config.read(twconfig)



# Variables for forming URL.
NUMBER = int(config["DEFAULT"]["last_file"])
PGN_PATH = config["DEFAULT"]["path_to_pgn_files"]


parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
parser.add_argument("-v", "--verbose", help="Enable output in console",
                    action="store_true")
group.add_argument("-c", "--check", help="Check if updates available",
                    action="store_true")
group.add_argument("-u", "--update", help="Download updates",
                    action="store_true")
group.add_argument("-m", "--merge", help="Download updates, merge them into one file",
                    action="store_true")
args = parser.parse_args()

verbose_flag = True if args.verbose else False


def form_twic_url(num):
    BASE_TWIC_URL = "http://www.theweekinchess.com/zips/twic"
    END_TWIC_URL = "g.zip"
    url = "".join((BASE_TWIC_URL, str(num), END_TWIC_URL))
    return url

def check_updates(verbosity=True):
    url_for_request = form_twic_url(NUMBER)
    request_code = urllib.request.urlopen(url_for_request).getcode()
    if request_code == 200:
        if verbosity:
            print("Some updates available!")
    else:
        if verbosity:
            print("No updates detected.")
    exit(0)

def do_update(merge=False):
    # Not implemented yet.
    pass
#     os.chdir(twdata_dir)
#     data_content = os.listdir()
#     if data_content:
#         for exfile in data_content:
#             if exfile.lower().endswith(".pgn")

if args.check:
    check_updates()
elif args.update:
    do_update()
elif args.merge:
    do_update(merge=True)

def extract_pgn_files(path, verbosity=False):
    os.chdir(path)
    ziplist = os.listdir()
    for z in ziplist:
        if zipfile.is_zipfile(z):
            if verbosity:
                print("Extracting %s..." % z)
            zname = zipfile.ZipFile(z)
            zname.extractall()
            zname.close()
            if verbosity:
                print("Deleting zip-archive: %s..." % z)
            os.remove(z)


def make_one_pgn(pgnpath):
    os.chdir(PGN_PATH)
    pgnlist = os.listdir()
    with open(pgnpath, "wb") as bigpgn:
        for pgn in pgnlist:
            with open(pgn, "rb") as pgncontent:
                shutil.copyfileobj(pgncontent, bigpgn, 1024*1024*10)

def main(num, pgn_path, verbosity=False):
    
    while True:
        url_for_download = form_twic_url(num)
        filename = "".join(("twic",str(num),"g.zip"))
        try:
            if verbosity:
                print("Trying to download %s..." % filename)
            if os.path.exists(os.path.join(pgn_path, filename)):
                if verbosity:
                    print("%s already exists. Skipped." % filename)
            else:
                response = urllib.request.urlopen(url_for_download)
                data = response.read()
                new_file = os.path.join(pgn_path,filename)
                data_file = open(new_file, "wb")
                data_file.write(data)
                data_file.close()
                if verbosity:
                    print("%s saved." % filename)
            num += 1
        except urllib.error.HTTPError:
            # HTTP Error 404: file not found on the server.
            # Here we must abort trying to download new files.
            if verbosity:
                print("No such file: %s" % filename)
                print("All downloads finished. Exiting...")
            break
    extract_pgn_files(pgn_path, verbosity)
    make_one_pgn("twic.pgn")


if __name__ == "__main__":
    main(NUMBER, PGN_PATH, verbose_flag)

    

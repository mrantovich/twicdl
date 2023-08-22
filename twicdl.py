#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# twicdl: TWIC (The Week in Chess) Downloader


import os
import configparser
import argparse
import shutil
import urllib.request
import zipfile
from sys import exit, argv, stderr, platform

if platform == 'win32':
    user_home = os.environ['APPDATA']
else:
    user_home = os.path.expanduser("~")

def write_config(configpath, num, path_to_pgn_files, twic_pgn):
    config["DEFAULT"] = {"last_file" : num,
                         "path_to_pgn_files" : path_to_pgn_files,
                         "twic_pgn" : twic_pgn
                        }
    with open(configpath, "w") as twconf:
        config.write(twconf)

# Check if data dir exists. Create if not.
if platform == 'win32':
    twdata_dir = os.path.join(os.path.expanduser("~"), "TWICDL")
else:
    twdata_dir = os.path.join(user_home, ".local/share/twicdl")
if not os.path.exists(twdata_dir):
    os.makedirs(twdata_dir)
big_twic_pgn = os.path.join(twdata_dir, "TWIC.pgn")

# Read config file or create new one if not exists.
config = configparser.ConfigParser()
if platform == 'win32':
    twconfig_dir = os.path.join(user_home, "TWICDL")
else:
    twconfig_dir = os.path.join(user_home, ".config/twicdl")
twconfig = os.path.join(twconfig_dir, "twicdl.ini")
if not os.path.exists(twconfig):
    os.makedirs(twconfig_dir, exist_ok=True)
    write_config(twconfig, "1497", twdata_dir, big_twic_pgn)
config.read(twconfig)

# Variables for forming URL.
NUMBER = int(config["DEFAULT"]["last_file"])
PGN_PATH = config["DEFAULT"]["path_to_pgn_files"]
BIG_TWIC = config["DEFAULT"]["twic_pgn"]


parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
parser.add_argument("-v",
                    "--verbose",
                    help="Enable output in console",
                    action="store_true")
group.add_argument("-c",
                   "--check",
                   help="Check if updates available",
                   action="store_true")
group.add_argument("-u",
                   "--update",
                   help="Download updates and merge them into one file",
                   action="store_true")
if len(argv) == 1:
    parser.print_help(stderr)
    exit(1)
args = parser.parse_args()


def form_twic_url(num):
    BASE_TWIC_URL = "http://www.theweekinchess.com/zips/twic"
    END_TWIC_URL = "g.zip"
    url = "".join((BASE_TWIC_URL, str(num), END_TWIC_URL))
    return url

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
    # Check if TWIC.pgn file already exists and delete it.
    if os.path.exists(pgnpath):
        os.remove(pgnpath)
    pgnlist = os.listdir()
    with open(pgnpath, "wb") as bigpgn:
        for pgn in pgnlist:
            with open(pgn, "rb") as pgncontent:
                shutil.copyfileobj(pgncontent, bigpgn, 1024*1024*10)

def check_updates(get_count=False, verbosity=False):
    update_counter = 0
    num = NUMBER
    is_there_updates = False
    while True:
        url_for_request = form_twic_url(num)
        try:
            req = urllib.request.Request(url_for_request,
                                         headers = {
                                             'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
                                         })
            request_code = urllib.request.urlopen(req).getcode()
            if request_code == 200:
                is_there_updates = True
                if get_count:
                    update_counter += 1
                    num += 1
                else:
                    break
        except urllib.error.HTTPError as err:
            if err.code == 404:
                break
    if is_there_updates:
        if get_count:
            if verbosity:
                print("There is %s file(s) to update!" % update_counter)
            return True
    else:
        if verbosity:
            print("No updates detected.")
        return False
    exit(0)


def do_update(start_num, verbosity=False):
    num = start_num
    os.chdir(twdata_dir)
    data_content = os.listdir()
    while True:
        num_filename = "".join(("twic", str(num), ".pgn"))
        if num_filename in data_content:
            if verbosity:
                print("%s already exists! Nothing to do." % num_filename)
            num += 1
        else:
            url_for_download = form_twic_url(num)
            filename = "".join(("twic",str(num),"g.zip"))
            try:
                if verbosity:
                    print("Trying to download %s..." % filename)
                if os.path.exists(os.path.join(PGN_PATH, filename)):
                    if verbosity:
                        print("%s already exists. Skipped." % filename)
                else:
                    req = urllib.request.Request(url_for_download,
                                         headers = {
                                             'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
                                         })
                    response = urllib.request.urlopen(req)
                    data = response.read()
                    new_file = os.path.join(PGN_PATH,filename)
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
                    print("All downloads finished.")
                break
    extract_pgn_files(PGN_PATH, verbosity)
    big_twic_pgn = os.path.join(twdata_dir, "TWIC.pgn")
    write_config(twconfig, num, twdata_dir, big_twic_pgn)
    if verbosity:
        print("Merging files...")
    make_one_pgn(BIG_TWIC)
    if verbosity:
        print("All done. Exiting...")


if args.check:
    check_updates(get_count=True, verbosity=args.verbose)
elif args.update:
    do_update(NUMBER, verbosity=args.verbose)



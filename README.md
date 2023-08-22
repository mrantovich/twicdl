# twicdl: The Week in Chess Downloader

## What is twicdl?
It's simple program for downloading PGN updates from site [The Week in Chess](https://theweekinchess.com/).\
It has command line interface for the time being but there will be GUI as well.

## How to use twicdl?
*On linux*\
Type `./twicdl.py --help` to see available keys.

*On Windows*\
Type `python .\twicdl.py --help` to see available keys.

There is verbosity option to show progress of running script.\
Just add `--verbosity` or `-v` to make output more informative.\
By default script is silent.

To check if there any updates type `./twicdl.py --check --verbosity`\
Script will say if there any files to update and how many.

To update PGN database type `./twicdl.py --update --verbosity`\
Files will be downloaded and merge into one big PGN file.\
It stores as TWIC.pgn in `~/.local/share/twicdl` (on Linux) or `$HOME\TWICDL` (on Windows).

## What else?
Program is in development.\
To contact a developer drop email on: mrantovich@gmail.com

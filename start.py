import sqlite3
import sys
from Tracker.ParserAPI.parser import *


def main():
    args = sys.argv[1::]
    parse(args)

if __name__ == '__main__':
    main()
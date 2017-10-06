#!/usr/bin/env python
import sys
#from src import main
import main

if __name__ == '__main__':
    sys.exit(main.run(sys.argv[1:]) or 0)
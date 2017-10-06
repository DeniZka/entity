#!/usr/bin/env python3

import sys

if __name__ == '__main__':
    from code import main

    sys.exit(main.run(sys.argv[1:]) or 0)
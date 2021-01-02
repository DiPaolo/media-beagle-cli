#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from file_analyzer import *

if __name__ == '__main__':
    print_ffmpeg_version()

    parser = argparse.ArgumentParser(description='Print information about media files.')
    parser.add_argument('qwe', metavar='dir', type=str, help='a directory where to start scanning')

    args = parser.parse_args()

    analyze_dir(args.qwe)

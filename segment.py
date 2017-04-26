"""
Program to read in INKML files and segment symbols

@author: Ajinkya Dhaigude (ad8454@rit.edu)
@author: Supriya Godge (spg5835@rit.edu)
"""

import sys
import os
import re
from bs4 import BeautifulSoup
import segment_read_files as s_read_files


def main(ar):
    all_files = s_read_files.get_all_files_coords(ar)
    


if __name__ == '__main__':
    ar = sys.argv
    if len(ar) == 2:
        main(ar[1])
    else:
        print('Incorrect arguments. Usage: segment.py <path to inkml files>')

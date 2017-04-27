"""
Program to read in INKML files and segment symbols

@author: Ajinkya Dhaigude (ad8454@rit.edu)
@author: Supriya Godge (spg5835@rit.edu)
"""

import sys
import os
import re
from bs4 import BeautifulSoup
import segment_read_files as sr_files
import pattern_rec_utils as pr_utils
import segment_extract_features as se_features


def main(ar):

    # get a list of Inkml objects
    all_inkml = sr_files.get_all_inkml_files(ar)

    # maximum scaled y coordinate
    max_coord = 100

    # scale coordinates in all Inkml objects
    pr_utils.scale_all_inkml(all_inkml, max_coord)





if __name__ == '__main__':
    ar = sys.argv
    if len(ar) == 2:
        main(ar[1])
    else:
        print('Incorrect arguments. Usage: segment.py <path to inkml files>')

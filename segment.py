"""
Program to read in INKML files and segment symbols

@author: Ajinkya Dhaigude (ad8454@rit.edu)
@author: Supriya Godge (spg5835@rit.edu)
"""

import sys
import segment_read_files as sr_files
import pattern_rec_utils as pr_utils
import segment_extract_features as se_features


def main(ar):

    max_coord = 100

    # get a list of Inkml objects
    all_inkml = sr_files.get_all_inkml_files(ar)

    # scale coordinates in all Inkml objects
    pr_utils.scale_all_inkml(all_inkml, max_coord)

    # segment into objects
    se_features.rough_trial(all_inkml)

    # scale each segmented object
    pr_utils.scale_all_segments(all_inkml, max_coord)

    # view symbols
    pr_utils.print_view_symbols_html(all_inkml, max_coord)

    #pr_utils.print_to_lg(all_inkml)



if __name__ == '__main__':
    ar = sys.argv
    if len(ar) == 2:
        main(ar[1])
    else:
        print('Incorrect arguments. Usage: segment.py <path to inkml files>')

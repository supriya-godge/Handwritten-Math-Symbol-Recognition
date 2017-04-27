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

    all_inkml = get_scaled_inkml(ar, 100)

    se_features.rough_trial(all_inkml)

    pr_utils.print_to_lg(all_inkml)



def get_scaled_inkml(ar, max_coord=100):
    """
    Take in a root directory path and return a list
    of Inkml objects with scaled coordinates
    representing each inkml file found in the root
    path.

    :param ar: Root directory path
    :param max_coord: maximum scaled y coordinate. Default is 100
    :return: list of Inkml objects
    """

    # get a list of Inkml objects
    all_inkml = sr_files.get_all_inkml_files(ar)

    # scale coordinates in all Inkml objects
    pr_utils.scale_all_inkml(all_inkml, max_coord)

    return all_inkml


if __name__ == '__main__':
    ar = sys.argv
    if len(ar) == 2:
        main(ar[1])
    else:
        print('Incorrect arguments. Usage: segment.py <path to inkml files>')

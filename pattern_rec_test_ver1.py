"""
Program to read in INKML files and segment symbols

@author: Ajinkya Dhaigude (ad8454@rit.edu)
@author: Supriya Godge (spg5835@rit.edu)
"""

import time
import pattern_rec_read_files as pr_files
import pattern_rec_utils as pr_utils
import segment_feature_extractor as seg_fe
import classify_feature_extractor as cfe
import parsing_feature_extractor as pfe
import classifiers
from sklearn.externals import joblib
import sys


def main(ar):
    """
    Run the program with parser version 1
    """

    max_coord = 100

    path_lg = ar[1]

    # load the trained model
    print('Reading model into memory')
    parser_weights = joblib.load(open(ar[2], "rb"))   # read trained parser model

    # get a list of Inkml objects
    print('Reading files into memory')
    all_inkml = pr_files.get_all_inkml_files(ar[0], True)

    # scale coordinates in all Inkml objects
    print('Scaling expression coordinates')
    pr_utils.scale_all_inkml(all_inkml, max_coord)

    # scale each segmented object
    print('Scaling symbol coordinates')
    pr_utils.scale_all_segments(all_inkml, max_coord)

    pr_utils.move_coords_to_objects(all_inkml, pfe)

    feature_matrix = pfe.feature_extractor(all_inkml)
    predicted_labels, probability = classifiers.random_forest_test_parsing(parser_weights.RF, feature_matrix)

    pr_utils.assign_parsing_labels(all_inkml, predicted_labels,probability)

    pr_utils.MST(all_inkml)

    pr_utils.print_to_file(all_inkml, ar[1])


if __name__ == '__main__':
    ar = sys.argv
    if len(ar) == 4:
        main(ar[1:])
    else:
        print('Incorrect arguments. \nUsage: segment_test.py <path to inkml files> <path to output dir> '
              '<parser model file>')
        ar = input('Enter args: ').split(' ')   #testing_inkml test_out parse_weights.p
        main(ar)

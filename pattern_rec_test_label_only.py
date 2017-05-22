"""
Program to read in INKML files and segment symbols

@author: Ajinkya Dhaigude (ad8454@rit.edu)
@author: Supriya Godge (spg5835@rit.edu)
"""

import winsound
import pattern_rec_read_files as pr_files
import pattern_rec_utils as pr_utils
import segment_feature_extractor as seg_fe
import classify_feature_extractor as cfe
import parsing_feature_extractor as pfe
import classifiers
from sklearn.externals import joblib
import sys
import trained_weights
import numpy as np
import time


def main(ar):
    max_coord = 100
    path = ar[0]
    path_lg = ar[1]

    # get a list of Inkml objects
    print('Reading files into memory')
    all_inkml = pr_files.get_all_inkml_files(path, True, path_lg)

    print('Scaling symbol coordinates')
    pr_utils.scale_all_segments(all_inkml, max_coord)

    pr_utils.move_coords_to_objects(all_inkml, pfe)

    parse_train(all_inkml, max_coord)


def parse_train(all_inkml, max_coord):
    print('Start feature extraction for parsing..')
    start = time.time()
    feature_matrix, truth_labels = pfe.feature_extractor(all_inkml, training=True)
    end = time.time()
    print("Time taken to extract the features for parsing:", round((end - start) / 60), "min")

    #np.savetxt('parsing_feature_matrix.csv', feature_matrix, delimiter=',')

    parser_weights = joblib.load(open('parse_weights_scale.p', "rb"))
    predicted_labels, probability = classifiers.random_forest_test_parsing(parser_weights.RF, feature_matrix)

    pr_utils.assign_parsing_labels(all_inkml, predicted_labels, probability)

    # pr_utils.MST(all_inkml)

    pr_utils.print_to_file(all_inkml, "label_only")


if __name__ == '__main__':
    ar = sys.argv
    if len(ar) == 3:
        main(ar[1:])
    else:
        print('Incorrect arguments.\nUsage: pattern_rec_train_label_only.py <path to inkml files> <path to lg files>'
              '\nREMEMBER to set parser weights.')
        ar = input('Enter args: ').split()
        main(ar)
        winsound.Beep(300, 2000)

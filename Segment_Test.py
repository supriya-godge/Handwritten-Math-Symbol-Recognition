"""
Program to read in INKML files and segment symbols

@author: Ajinkya Dhaigude (ad8454@rit.edu)
@author: Supriya Godge (spg5835@rit.edu)
"""

import sys
import pattern_rec_read_files as pr_files
import pattern_rec_utils as pr_utils
import segment_feature_extractor as seg_fe
import classify_feature_extractor as cfe
import classifiers
from classifier_trained_weights import TrainedWeights
from sklearn.externals import joblib
import sys
import Trained_weight

def main(ar):

    max_coord = 100

    #Load the traning data
    pfile = sys.argv[2]
    data = joblib.load(open(pfile, "rb"))

    # get a list of Inkml objects
    all_inkml = pr_files.get_all_inkml_files(ar, True)

    # scale coordinates in all Inkml objects
    pr_utils.scale_all_inkml(all_inkml, max_coord)

    # segment into objects
    #seg_fe.rough_trial(all_inkml)

    # scale each segmented object
#    pr_utils.scale_all_segments(all_inkml, max_coord)
    test_matrix =seg_fe.feature_extractor(all_inkml)
    results = classifiers.random_forest_test(data.RF, test_matrix[:, :-1], test_matrix[:, -1])
    print_to_file('rf-results.csv', results)


def print_to_file(fileName, results):

    with open(fileName, 'w') as new_file:
        for inkml in results:
            new_file.write(inkml + '\n')

    print('File written to disk: ' + fileName)


if __name__ == '__main__':
    ar = sys.argv
    if len(ar) == 3:
        main(ar[1])
    else:
        print('Incorrect arguments. \nUsage: segment.py <path to inkml files> \neg: segment.py TestINKML')
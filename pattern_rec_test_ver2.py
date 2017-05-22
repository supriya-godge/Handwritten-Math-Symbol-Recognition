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
    Run the program with parser version 2
    """

    max_coord = 100

    # load the trained models
    print('Reading models into memory')
    segment_weights = joblib.load(open(ar[2], "rb"))    # read trained segmentation model
    classify_weights = joblib.load(open(ar[3], "rb"))   # read trained classification model
    parser_weights = joblib.load(open(ar[4], "rb"))   # read trained parser model

    # get a list of Inkml objects
    print('Reading files into memory')
    all_inkml = pr_files.get_all_inkml_files(ar[0], False)

    # scale coordinates in all Inkml objects
    print('Scaling expression coordinates')
    pr_utils.scale_all_inkml(all_inkml, max_coord)

    # segment into objects
    print('Start feature extraction for segmentation..')
    feature_matrix, strokes_to_consider = seg_fe.feature_extractor(all_inkml)
    predicted_labels = classifiers.random_forest_test(segment_weights.RF, feature_matrix)

    print('Assigning segmentation labels..')
    pr_utils.assign_segmentation_labels(all_inkml, predicted_labels, strokes_to_consider)

    # scale each segmented object
    print('Scaling symbol coordinates')
    pr_utils.scale_all_segments(all_inkml, max_coord)

    # classify each segmented object
    print('Start feature extraction for classifier..')
    online_features = [cfe.OnlineFeature, cfe.polarFeature, cfe.endPointToCenter,cfe.polarFeature]
    offline_functions = [cfe.zoning, cfe.XaxisProjection, cfe.YaxisProjection, cfe.DiagonalProjections]
    feature_matrix, truth_labels = cfe.get_training_matrix(all_inkml,
                                                            max_coord,
                                                            online_features,
                                                            offline_functions)

    predicted_labels = classifiers.random_forest_test(classify_weights.RF, feature_matrix)

    print('Assigning classifier labels..')
    pr_utils.assign_classification_labels(all_inkml, predicted_labels)


    print('Reverting back to expression scaling..')
    for inkml in all_inkml:
        inkml.revert_strokes()      # revert back to expression scaling

    pr_utils.move_coords_to_objects(all_inkml, pfe)

    print('Start feature extraction for parsing')
    feature_matrix = pfe.feature_extractor(all_inkml)
    predicted_labels, probability = classifiers.random_forest_test_parsing(parser_weights.RF, feature_matrix)

    print('Assigning parser labels..')
    pr_utils.assign_parsing_labels(all_inkml, predicted_labels, probability)

    print("Computing maximum spanning tree")
    start = time.time()
    pr_utils.create_MST_bruteForce(all_inkml)
    end = time.time()
    print("Time taken for MST:", (end - start) / 60, "min")

    pr_utils.print_to_file(all_inkml, ar[1])


if __name__ == '__main__':
    ar = sys.argv
    if len(ar) == 6:
        main(ar[1:])
    else:
        print('Incorrect arguments. \nUsage: pattern_rec_test_ver2.py <path to inkml files> <path to output dir> '
              '<segmentation model file> <classification model file> <parser model file>')
        ar = input('Enter args: ').split(' ')
        main(ar)

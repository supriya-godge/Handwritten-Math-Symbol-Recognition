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
    mode = int(ar[2])

    # get a list of Inkml objects
    print('Reading files into memory')
    all_inkml = pr_files.get_all_inkml_files(path, True, path_lg)

    if not mode or mode == 1:   # not 0 = True
        segment_train(all_inkml, max_coord)

    print('Scaling symbol coordinates')
    pr_utils.scale_all_segments(all_inkml, max_coord)

    if not mode or mode == 2:
        classify_train(all_inkml, max_coord)

    pr_utils.move_coords_to_objects(all_inkml, pfe)

    if not mode or mode == 3:
        parse_train(all_inkml, max_coord)


def parse_train(all_inkml, max_coord):
    print('Start feature extraction for parsing..')
    start = time.time()
    feature_matrix, truth_labels = pfe.feature_extractor(all_inkml, training=True)
    end = time.time()
    print("Time taken to extract the features for parsing:", round((end - start) / 60), "min")

    #np.savetxt('parsing_feature_matrix.csv', feature_matrix, delimiter=',')

    start = time.time()
    rf = classifiers.random_forest_train(feature_matrix,
                                         truth_labels)
    end = time.time()
    print("Time taken to train Random Forest:", round((end - start) / 60, 2), "min")

    joblib.dump(trained_weights.TrainedWeights(rf), open('parse_weights_psc.p', 'wb'), compress=True)
    print('Training complete. Model file saved to disk.')


def segment_train(all_inkml, max_coord):

    # scale coordinates in all Inkml objects
    print('Scaling expression coordinates')
    pr_utils.scale_all_inkml(all_inkml, max_coord)

    #print('Start pre-processing for segmentation..')
    #pr_utils.preprocessing(all_inkml)

    # segment into objects
    print('Start feature extraction for segmentation..')
    start = time.time()
    feature_matrix, truth_labels = seg_fe.feature_extractor(all_inkml, training=True)
    end = time.time()
    print("Time taken to extract the features for segmentation:", round((end - start)/60), "min")

    #np.savetxt('segment_feature_matrix.csv', feature_matrix, delimiter=',')

    start=time.time()
    rf = classifiers.random_forest_train(feature_matrix,
                                         truth_labels)
    end = time.time()
    print("Time taken to train Random Forest:", round((end - start)/60, 2), "min")

    joblib.dump(trained_weights.TrainedWeights(rf), open('segment_weights.p', 'wb'), compress=True)
    print('Training complete. Model file saved to disk.')


def classify_train(all_inkml, max_coord):
    # get feature matrix for classifier training
    print('Start feature extraction for classifier..')

    start = time.time()
    online_features = [cfe.OnlineFeature, cfe.polarFeature, cfe.endPointToCenter]
    offline_functions = [cfe.zoning, cfe.XaxisProjection, cfe.YaxisProjection, cfe.DiagonalProjections]
    feature_matrix, truth_labels = cfe.get_training_matrix(all_inkml,
                                                            max_coord,
                                                            online_features,
                                                            offline_functions)

    end = time.time()
    print("Time taken to extract the features for classification:", round((end-start)/60, 2), "min")

    start = time.time()
    rf = classifiers.random_forest_train(feature_matrix,
                                         truth_labels)
    end = time.time()
    print("Time taken to train Random Forest:", round((end - start)/60), "min")

    joblib.dump(trained_weights.TrainedWeights(rf), open('classify_weights.p', 'wb'), compress=True)
    print('Training complete. Model file saved to disk.')

    # view symbols
    #pr_utils.print_view_symbols_html(all_inkml, max_coord)

    #pr_utils.print_to_lg(all_inkml)


if __name__ == '__main__':
    ar = sys.argv
    if len(ar) == 4:
        main(ar[1:])
    else:
        print('Incorrect arguments.\nUsage: pattern_rec_train.py <path to inkml files> <path to lg files>'
              ' <0:all 1:segment 2:classify 3:parse>')
        ar = input('Enter args: ').split()
        main(ar)
        winsound.Beep(300, 2000)

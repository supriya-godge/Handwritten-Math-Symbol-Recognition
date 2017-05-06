"""
Program to read in INKML files and segment symbols

@author: Ajinkya Dhaigude (ad8454@rit.edu)
@author: Supriya Godge (spg5835@rit.edu)
"""

import winsound
import sys
import pattern_rec_read_files as pr_files
import pattern_rec_utils as pr_utils
import segment_feature_extractor as seg_fe
import classify_feature_extractor as cfe
import classifiers
from sklearn.externals import joblib
import sys
import trained_weights
import numpy as np
import time

def main(ar,flag):
    max_coord = 100

    # get a list of Inkml objects
    print('Reading files into memory')
    all_inkml = pr_files.get_all_inkml_files(ar, True)
    if flag == 1:
        segment_train(all_inkml,max_coord)
    elif flag == 2:
        classify_train(all_inkml,max_coord)
    else:
        segment_train(all_inkml, max_coord)
        classify_train(all_inkml, max_coord)

def segment_train(all_inkml, max_coord):
    # scale coordinates in all Inkml objects
    print('Scaling expression coordinates')
    pr_utils.scale_all_inkml(all_inkml, max_coord)
    print('Start preproseccing for segmentation..')
    pr_utils.preprocessing(all_inkml)

    # segment into objects
    print('Start feature extraction for segmentation..')
    start = time.time()
    feature_matrix, truth_labels = seg_fe.feature_extractor(all_inkml, training=True)
    end = time.time()
    print("Time taken to extract the features for segmentation:", (end - start)/60, "min")

    start=time.time()
    rf = classifiers.random_forest_train(feature_matrix,
                                         truth_labels)
    end=time.time()
    print("Time taken to train Random Forest:", round((end - start)/60, 2), "min")

    joblib.dump(trained_weights.TrainedWeights(rf), open('all_segment_weights.p', 'wb'), compress=True)
    print('Training complete. Model file saved to disk.')


def classify_train(all_inkml, max_coord):
    # scale each segmented object
    print('Scaling symbol coordinates')
    pr_utils.scale_all_segments(all_inkml, max_coord)

    # get feature matrix for classifier training
    print('Start feature extraction for classifier..')

    start = time.time()
    online_features = [cfe.OnlineFeature,cfe.polarFeature,cfe.endPointToCenter]
    offline_functions = [cfe.zoning, cfe.XaxisProjection, cfe.YaxisProjection, cfe.DiagonalProjections]
    start=time.time()
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
    print("Time taken to train Random Forest:", (end - start)/60, "min")

    joblib.dump(trained_weights.TrainedWeights(rf), open('all_classify_weights.p', 'wb'), compress=True)
    print('Training complete. Model file saved to disk.')

    # view symbols
    #pr_utils.print_view_symbols_html(all_inkml, max_coord)

    #pr_utils.print_to_lg(all_inkml)


if __name__ == '__main__':
    ar = sys.argv
    if len(ar) == 3:
        main(ar[1],int(ar[2])) # TrainINKML/extension
    else:
        print('Incorrect arguments. \nUsage: segment.py <path to inkml files> <1: segment, 2:classify>')
        ar = input('Enter args: ').split()
        main(ar[0], int(ar[1]))
        winsound.Beep(300, 2000)
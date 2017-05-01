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
    # get a list of Inkml objects
    all_inkml = pr_files.get_all_inkml_files(ar, True)


    # scale coordinates in all Inkml objects
    pr_utils.scale_all_inkml(all_inkml, max_coord)
    # segment into objects
    #seg_fe.rough_trial(all_inkml)
    training_matrix = seg_fe.feature_extractor(all_inkml)
    #print(training_matrix)
    rf = classifiers.random_forest_train(training_matrix[:, :-1],
                                         training_matrix[:, -1])
    joblib.dump(Trained_weight.TrainWeight(rf), open("TrainWeightFile.p", "wb"), compress=True)
    '''
    # scale each segmented object
    pr_utils.scale_all_segments(all_inkml, max_coord)


    # get feature matrix
    online_features = [cfe.OnlineFeature]
    offline_functions = [cfe.XaxisProjection]
    #offline_functions = [cfe.zoning, cfe.XaxisProjection, cfe.YaxisProjection, cfe.DiagonalProjections]
    training_matrix, truth_labels = cfe.get_training_matrix(all_inkml,
                                                            max_coord,
                                                            online_features,
                                                            offline_functions)

    rf = classifiers.random_forest_train(training_matrix,
                                         truth_labels)

    kd = classifiers.kd_tree_train(training_matrix[:, :-1])

    joblib.dump(TrainedWeights(rf, kd), open('model_trained.p', 'wb'), compress=True)

    # view symbols
    #pr_utils.print_view_symbols_html(all_inkml, max_coord)

    #pr_utils.print_to_lg(all_inkml)
    '''



if __name__ == '__main__':
    ar = sys.argv
    if len(ar) == 2:
        main(ar[1]) # TrainINKML/extension
    else:
        print('Incorrect arguments. \nUsage: segment.py <path to inkml files> \neg: segment.py TrainINKML')
        ar = input('Enter args: ')
        main(ar)

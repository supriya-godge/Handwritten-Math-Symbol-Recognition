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
from sklearn.externals import joblib
import sys
import trained_weights

def main(ar):
    max_coord = 100

    # get a list of Inkml objects
    all_inkml = pr_files.get_all_inkml_files(ar, True)

    # scale coordinates in all Inkml objects
    pr_utils.scale_all_inkml(all_inkml, max_coord)

    # segment into objects
    feature_matrix, truth_labels = seg_fe.feature_extractor(all_inkml)
    rf = classifiers.random_forest_train(feature_matrix,
                                         truth_labels)

    joblib.dump(trained_weights.TrainedWeights(rf), open('segment_weights.p', 'wb'), compress=True)

    # scale each segmented object
    pr_utils.scale_all_segments(all_inkml, max_coord)

    # get feature matrix for classifier training
    online_features = [cfe.OnlineFeature]
    offline_functions = [cfe.zoning, cfe.XaxisProjection, cfe.YaxisProjection, cfe.DiagonalProjections]
    feature_matrix, truth_labels = cfe.get_training_matrix(all_inkml,
                                                            max_coord,
                                                            online_features,
                                                            offline_functions)

    rf = classifiers.random_forest_train(feature_matrix,
                                         truth_labels)

    joblib.dump(trained_weights.TrainedWeights(rf), open('classify_weights.p', 'wb'), compress=True)

    print('Training complete. Model files saved to disk.')

    # view symbols
    #pr_utils.print_view_symbols_html(all_inkml, max_coord)

    #pr_utils.print_to_lg(all_inkml)



if __name__ == '__main__':
    ar = sys.argv
    if len(ar) == 2:
        main(ar[1]) # TrainINKML/extension
    else:
        print('Incorrect arguments. \nUsage: segment.py <path to inkml files>')
        ar = input('Enter args: ')
        main(ar)

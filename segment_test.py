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

def main(ar):

    max_coord = 100

    # load the trained models
    print('Reading models into memory')
    segment_weights = joblib.load(open(ar[1], "rb"))    # read trained segmentation model
    classify_weights = joblib.load(open(ar[2], "rb"))   # read trained classification model

    # get a list of Inkml objects
    print('Reading files into memory')
    all_inkml = pr_files.get_all_inkml_files(ar[0], False)

    # scale coordinates in all Inkml objects
    print('Scaling expression coordinates')
    pr_utils.scale_all_inkml(all_inkml, max_coord)

    # segment into objects
    print('Start feature extraction..')
    feature_matrix, truth_labels = seg_fe.feature_extractor(all_inkml)
    predicted_labels = classifiers.random_forest_test(segment_weights.RF, feature_matrix)
    assign_segmentation_labels(all_inkml, predicted_labels)

    # scale each segmented object
    print('Scaling symbol coordinates')
    pr_utils.scale_all_segments(all_inkml, max_coord)

    # classify each segmented object
    print('Start feature extraction..')
    online_features = [cfe.OnlineFeature,cfe.polarFeature,cfe.endPointToCenter]
    offline_functions = [cfe.zoning, cfe.XaxisProjection, cfe.YaxisProjection, cfe.DiagonalProjections]
    feature_matrix, truth_labels = cfe.get_training_matrix(all_inkml,
                                                            max_coord,
                                                            online_features,
                                                            offline_functions)
    predicted_labels = classifiers.random_forest_test(classify_weights.RF, feature_matrix)
    assign_classification_labels(all_inkml, predicted_labels)

    print_to_file(all_inkml, 'E:/PaternRec/Project2/test_out')


def assign_segmentation_labels(all_inkml, predicted_labels):

    label_idx = 0
    for inkml in all_inkml:
        current_segment = []
        for trace_id in inkml.strokes:
            current_segment.append(trace_id)

            is_last_stroke = trace_id == next(reversed(inkml.strokes))  # boolean flag set if trace_id is last stroke

            if is_last_stroke or predicted_labels[label_idx] == False:
                inkml.create_object(current_segment)
                current_segment = []

            label_idx += 1
        label_idx -= 1  # decrement label index after each file because last stroke is not part of predicted_labels


def assign_classification_labels(all_inkml, predicted_labels):
    label_idx = 0

    for inkml in all_inkml:
        symbol_count = {}
        for obj in inkml.objects:
            label_symbol = predicted_labels[label_idx]

            if label_symbol in symbol_count:
                symbol_count[label_symbol] += 1
            else:
                symbol_count[label_symbol] = 1

            object_id = label_symbol + '_' + str(symbol_count[label_symbol])
            obj.set_details(object_id, label_symbol)

            label_idx += 1


def print_to_file(all_inkml, path):

    for inkml in all_inkml:
        file_name = path + '/' + inkml.ui + '.lg'
        with open(file_name, 'w') as new_file:
            out = inkml.get_objects_str()
            new_file.write(out)

    print('Files written to disk')


if __name__ == '__main__':
    ar = sys.argv
    if len(ar) == 4:
        main(ar[1:])
    else:
        print('Incorrect arguments. \nUsage: segment_test.py <path to inkml files> '
              '<segmentation model file> <classification model file>')
        ar = input('Enter args: ').split(' ')
        main(ar)
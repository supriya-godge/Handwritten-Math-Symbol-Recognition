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
    all_inkml = pr_files.get_all_inkml_files(ar, False)

    # scale coordinates in all Inkml objects
    pr_utils.scale_all_inkml(all_inkml, max_coord)

    # segment into objects
    #seg_fe.rough_trial(all_inkml)

    # scale each segmented object
    # pr_utils.scale_all_segments(all_inkml, max_coord)

    feature_matrix, truth_labels = seg_fe.feature_extractor(all_inkml)
    predicted_labels = classifiers.random_forest_test(data.RF, feature_matrix)
    assign_labels(all_inkml, predicted_labels)
    print_to_file(all_inkml, 'test_out')



def assign_labels(all_inkml, predicted_labels):

    label_idx = 0
    for inkml in all_inkml:
        current_segment = []
        for trace_id in inkml.strokes:
            current_segment.append(trace_id)

            is_last_stroke = trace_id == next(reversed(inkml.strokes))  # boolean flag set if trace_id is last stroke
            print (all_inkml.index(inkml), len(all_inkml))
            if is_last_stroke or predicted_labels[label_idx] == 0:
                obj = inkml.create_object(current_segment)
                obj.set_details()
                current_segment = []

            label_idx += 1
        label_idx -= 1



def print_to_file(all_inkml, path):

    for inkml in all_inkml:
        file_name = path + '/' + inkml.ui + '.lg'
        with open(file_name, 'w') as new_file:
            out = inkml.get_objects_str()
            new_file.write(out)

    print('Files written to disk')


if __name__ == '__main__':
    ar = sys.argv
    if len(ar) == 3:
        main(ar[1])
    else:
        print('Incorrect arguments. \nUsage: segment.py <path to inkml files> \neg: segment.py TestINKML')
        ar = input('Enter args: ')
        main(ar)
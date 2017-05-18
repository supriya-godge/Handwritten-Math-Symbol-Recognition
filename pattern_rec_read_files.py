"""
Program to read in INKML files parse stroke coordinates

@author: Ajinkya Dhaigude (ad8454@rit.edu)
@author: Supriya Godge (spg5835@rit.edu)
"""

import os
import re
from bs4 import BeautifulSoup
from info_inkml import Inkml
import sys
import numpy as np


def get_all_inkml_files(ar, training=False, path_lg=None):
    """
    Recursively open each subdirectory and read each inkml
    file within. Return a list of Inkml objects created from
    the files.

    :param ar: path to inkml files
    :param training: set flag to read in ground truth values as well
    :param path_lg: path to lg files
    :return: list of Inkml objects
    """

    # get individual file path to each inkml file
    all_file_paths = get_all_file_paths(ar)

    # populate list with an Inkml object for each file
    all_inkml = []
    for file_path in all_file_paths:
        inkml = read_file(file_path, training, path_lg)
        if inkml is not None:
            all_inkml.append(inkml)

    return all_inkml


def read_file(file_path, training, path_lg):
    """
    Open and read an inkml file. Create an Inkml object with the
    parsed information.

    :param file_path: file path to inkml file
    :param training: set flag to read in ground truth values as well
    :param path_lg: path to lg files
    :return: Inkml object
    """

    # open and read file
    soup = BeautifulSoup(open(file_path), 'lxml')

    # parse file for UI. Return None if not found
    file_ui = soup.find('annotation', {'type': 'UI'})
    if file_ui is not None:
        file_ui = file_ui.string.strip('"')
    else:
        print('Skipping file: ', file_path)
        return None

    # UI does not match file name so get from file path
    file_ui = file_path.split('/')[-1]
    file_ui = file_ui.split('\\')[-1]
    if file_ui.endswith('.inkml'):
        file_ui = file_ui[:-6]
    else:
        print('Skipping file: ', file_path)
        return None

    # create Inkml object
    inkml = Inkml(file_ui)

    # add stroke information to Inkml object
    for trace in soup.find_all('trace'):
        stroke = trace.string.strip('\n').split(',')
        coords = []

        for point in stroke:
            point = [val for val in point.split(' ') if len(val) > 0]
            x = float(point[0])
            y = float(point[1])
            coords.append([x, y])

        inkml.add_stroke(trace.get('id'), coords)

    if training:
        path_lg += '/' + inkml.ui + '.lg'
        inkml = add_ground_truth(inkml, soup, path_lg)

    return inkml


def add_ground_truth(inkml, soup, path_lg):
    """
    Add ground truth values to inkml file
    """

    # set object ground truth values
    for trace_group in soup.find_all('tracegroup'):
        label = trace_group.find('annotation', {'type': 'truth'})
        obj_id = trace_group.find('annotationxml', recursive=False)
        if obj_id is None:
            continue

        obj_strokes = []
        for trace_view in trace_group.find_all('traceview'):
            obj_strokes.append(trace_view.get('tracedataref'))

        obj = inkml.create_object(obj_strokes)
        obj.set_details(obj_id.get('href'), label.string)

    # sort the newly created objects by trace_ids
    inkml.sort_objects()

    # set relation ground truth from lg files
    with open(path_lg, 'r') as lg_file:
        rel_lines = [line for line in lg_file.readlines() if line[0] == 'R' or line[0] == 'E']

    for line in rel_lines:
        line = line.split(',')
        obj1 = line[1].strip()
        obj2 = line[2].strip()
        rel_label = line[3].strip()
        inkml.create_relation(obj1, obj2, rel_label)

    return inkml



'''
def read_file_Traning(file_path):
    """
    Open and read an inkml file. Create an Inkml object with the
    parsed information.

    :param file_path: file path to inkml file
    :return: Inkml object
    """

    # open and read file
    soup = BeautifulSoup(open(file_path), 'lxml')

    # parse file for UI. Return None if not found
    file_truth = soup.find_all('annotation',{'type':'truth'})
    if file_truth is not None:
        symb=[]
        for f in file_truth:
            symb.append(f.string)
    else:
        print('Skipping file: ', file_path)
    return symb[2:]
'''


def get_all_file_paths(root_path):
    """
    Generate a list of all valid inkml file paths

    :param root_path: path to root directory
    :return: list of paths
    """

    all_file_paths = []
    # full string ending in .inkml
    regex = re.compile('.*\.inkml')

    # recursively open subdirs and filter inkml files
    for root, dirs, file_names in os.walk(root_path):
        inkml_files = filter(regex.match, file_names)
        for file in inkml_files:
            all_file_paths.append(root + '/' + file)

    return all_file_paths


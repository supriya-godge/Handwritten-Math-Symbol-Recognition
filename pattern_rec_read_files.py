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


def get_all_inkml_files(ar, training=False):
    """
    Recursively open each subdirectory and read each inkml
    file within. Return a list of Inkml objects created from
    the files.

    :param ar: path to inkml files
    :param training: set flag to read in ground truth values as well
    :return: list of Inkml objects
    """
    print("In read")

    # get individual file path to each inkml file
    #all_file_paths = get_all_file_paths(ar)
    all_file_paths = read_files_path(ar)
    print("Got all paths:",len(all_file_paths))
    # populate list with an Inkml object for each file
    all_inkml = []
    for file_path in all_file_paths:
        if training:
            inkml = read_training_file(file_path)
        else:
            inkml = read_file(file_path)
        if inkml is not None:
            all_inkml.append(inkml)

    return all_inkml


def read_training_file(file_path):
    """
    Open and read an inkml file along with ground truth values.
    Create an Inkml object with the parsed information.

    :param file_path: file path to inkml file
    :return: Inkml object
    """

    # TODO: merge with read_file()

    # open and read file
    soup = BeautifulSoup(open(file_path), 'lxml')

    # parse file for UI. Return None if not found
    file_ui = soup.find('annotation', {'type': 'UI'})
    if file_ui is not None:
        file_ui = file_ui.string
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


    # set ground truth values
    for trace_group in soup.find_all('tracegroup'):

        label = trace_group.find('annotation', {'type': 'truth'})
        obj_id = trace_group.find('annotationxml', recursive=False)
        if obj_id is None:
            continue

        obj_strokes = []
        for trace_view in trace_group.find_all('traceview'):
            obj_strokes.append(int(trace_view.get('tracedataref')))

        obj = inkml.create_object(obj_strokes)
        obj.set_details(obj_id.get('href'), label.string)

    return inkml


def read_file(file_path):
    """
    Open and read an inkml file. Create an Inkml object with the
    parsed information.

    :param file_path: file path to inkml file
    :return: Inkml object
    """

    # open and read file
    soup = BeautifulSoup(open(file_path), 'lxml')

    # parse file for UI. Return None if not found
    file_ui = soup.find('annotation', {'type': 'UI'})
    if file_ui is not None:
        file_ui = file_ui.string
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
    return inkml


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


def read_files_path(fileName):
    all_file_paths=[]
    with open(fileName) as fileName:
        for line in fileName:
            line = line.strip("\n")
            all_file_paths.append(line)
    return all_file_paths


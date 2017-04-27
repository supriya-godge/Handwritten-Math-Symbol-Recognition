"""
Program to read in INKML files parse stroke coordinates

@author: Ajinkya Dhaigude (ad8454@rit.edu)
@author: Supriya Godge (spg5835@rit.edu)
"""

import os
import re
from bs4 import BeautifulSoup
from info_inkml import Inkml


def get_all_inkml_files(ar):
    """
    Recursively open each subdirectory and read each inkml
    file within. Return a list of Inkml objects created from
    the files.

    :param ar: path to inkml files
    :return: list of Inkml objects
    """

    # get individual file path to each inkml file
    all_file_paths = get_all_file_paths(ar)

    # populate list with an Inkml object for each file
    all_inkml = []
    for file_path in all_file_paths:
        inkml = read_file(file_path)
        if inkml is not None:
            all_inkml.append(inkml)

    return all_inkml


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
        inkml.add_stroke(trace.get('id'), trace.string)

    return inkml


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

"""
Program to read in INKML files parse stroke coordinates

@author: Ajinkya Dhaigude (ad8454@rit.edu)
@author: Supriya Godge (spg5835@rit.edu)
"""

import sys
import os
import re
from bs4 import BeautifulSoup


def get_all_files_coords(ar):
    """

    :param ar: path to inkml files
    :return: dict{file_ui: [(trace id, trace coordinates)]}
    """

    # get individual file path to each inkml file
    all_file_paths = get_all_file_paths(ar)

    # dict of files: file_ui: all_traces[]
    all_files = {}
    for file_path in all_file_paths:
        file_ui, all_traces = read_file(file_path)
        if file_ui is None:
            continue
        all_files[file_ui] = all_traces
        #print(file_ui)

    return all_files


def read_file(file_path):
    soup = BeautifulSoup(open(file_path), 'lxml')

    file_ui = soup.find('annotation', {'type': 'UI'})
    if file_ui is not None:
        file_ui = file_ui.string
    else:
        print('Skipping file: ', file_path)
        return None, None


    # list of tuples: ((str)trace id, trace coordinates)
    all_traces = []
    for trace in soup.find_all('trace'):
        all_traces.append((trace.get('id'), trace.string))

    return file_ui, all_traces


def get_all_file_paths(root_path):
    all_file_paths = []
    # full string ending in .inkml
    regex = re.compile('.*\.inkml')

    # recursively open subdirs and filter inkml files
    for root, dirs, file_names in os.walk(root_path):
        inkml_files = filter(regex.match, file_names)
        for file in inkml_files:
            all_file_paths.append(root + '/' + file)

    return all_file_paths

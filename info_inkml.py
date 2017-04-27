"""
Class file to store information about a .inkml file

@author: Ajinkya Dhaigude (ad8454@rit.edu)
@author: Supriya Godge (spg5835@rit.edu)
"""

import collections


class Inkml:
    """
    Class to contain information about each inkml file.
    """

    def __init__(self, ui):
        self.ui = ui
        self.strokes = collections.OrderedDict()

    def add_stroke(self, trace_id, coords):
        self.strokes[trace_id] = coords

    def update_strokes(self, scaled_coords):
        for index, trace_id in enumerate(self.strokes):
            self.strokes[trace_id] = scaled_coords[index]


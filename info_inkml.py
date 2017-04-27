"""
Class file to store information about a .inkml file

@author: Ajinkya Dhaigude (ad8454@rit.edu)
@author: Supriya Godge (spg5835@rit.edu)
"""

import collections
from info_symbol_object import SymbolObject


class Inkml:
    """
    Class to contain information about each inkml file.
    """

    def __init__(self, ui):
        self.ui = ui
        self.strokes = collections.OrderedDict()
        self.objects = []

    def add_stroke(self, trace_id, coords):
        self.strokes[trace_id] = coords

    def update_strokes(self, scaled_coords):
        for index, trace_id in enumerate(self.strokes):
            self.strokes[trace_id] = scaled_coords[index]

    def create_object(self, trace_ids):
        obj = SymbolObject(trace_ids)
        self.objects.append(obj)

    def get_objects_str(self):
        result = ''
        for obj in self.objects:
            result += 'O , {}, {}, {}, {}\n'.format(obj.object_id, obj.label,
                                              obj.weight, ', '.join(trace_id for trace_id in obj.trace_ids))

        return result


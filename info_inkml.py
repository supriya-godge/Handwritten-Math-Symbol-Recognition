"""
Class file to store information about a .inkml file

@author: Ajinkya Dhaigude (ad8454@rit.edu)
@author: Supriya Godge (spg5835@rit.edu)
"""

import collections
from info_symbol_object import SymbolObject
from info_symbol_relation import SymbolRelation


class Inkml:
    """
    Class to contain information about each inkml file.
    """

    def __init__(self, ui):
        self.ui = ui
        self.strokes = collections.OrderedDict()
        self.objects = []
        self.relations = []

    def add_stroke(self, trace_id, coords):
        self.strokes[trace_id] = coords

    def update_strokes(self, scaled_coords):
        for index, trace_id in enumerate(self.strokes):
            self.strokes[trace_id] = scaled_coords[index]

    def create_object(self, trace_ids):
        obj = SymbolObject(trace_ids)
        self.objects.append(obj)
        return obj

    def create_relation(self, object_id1=None, object_id2=None, label=None):
        rel = SymbolRelation(object_id1, object_id2, label)
        self.relations.append(rel)
        return rel

    def get_objects_str(self):
        result = ''
        for obj in self.objects:
            result += 'O, {}, {}, {}, {}\n'.format(obj.object_id, obj.label,
                                              obj.weight, ', '.join(trace_id for trace_id in obj.trace_ids))

        return result

    def get_relations_str(self):
        result = ''
        for rel in self.relations:
            result += 'EO, {}, {}, {}, {}\n'.format(rel.object1.object_id, rel.object2.object_id, rel.label, rel.weight)

        return result

    def sort_objects(self):
        # sort objects by trace_ids
        self.objects.sort(key=lambda x: float(min(x.trace_ids, key=float)))

    def __str__(self):
        return self.objects.__str__()

    def __repr__(self):
        return self.objects.__repr__()


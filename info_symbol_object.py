"""
Class file to store information about a symbol
represented as an Object.

@author: Ajinkya Dhaigude (ad8454@rit.edu)
@author: Supriya Godge (spg5835@rit.edu)
"""


class SymbolObject:
    """
    Class to contain information about each symbol Object
    """

    def __init__(self, trace_ids):
        self.object_id = None
        self.label = None
        self.weight = None
        self.trace_ids = trace_ids  # should be a list
        self.truth = None  # used by training set only

    def set_details(self, object_id, label, weight):
        self.object_id = object_id
        self.label = label
        self.weight = str(weight)

    def set_truth(self, truth):
        self.truth = truth



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

    def set_details(self, object_id='x', label='x', weight=1.0):
        self.object_id = object_id
        if label == ',':
            label = 'COMMA'
        self.label = label
        self.weight = str(weight)




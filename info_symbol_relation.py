"""
Class file to store information about symbol
Relationships.

@author: Ajinkya Dhaigude (ad8454@rit.edu)
@author: Supriya Godge (spg5835@rit.edu)
"""


class SymbolRelation:
    """
    Class to contain information about each symbol Relationship
    """

    def __init__(self, trace_ids):
        self.object_id1 = None
        self.object_id2 = None
        self.label = None
        self.weight = None

    def set_relation(self, object_id1='x', object_id2='x', label='Right', weight=1.0):
        self.object_id1 = object_id1
        self.object_id2 = object_id2
        self.label = label
        self.weight = str(weight)




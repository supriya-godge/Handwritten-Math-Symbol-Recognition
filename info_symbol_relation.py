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

    def __init__(self, object1, object2, label):
        self.object1 = object1
        self.object2 = object2
        self.label = label
        self.weight = -1.0

    def set_relation(self, object1, object2, label):
        self.object1 = object1
        self.object2 = object2
        self.label = label

    def __str__(self):
        return self.object1.object_id+" "+self.object2.object_id+":"+self.label+":"+str(self.weight)

    def __repr__(self):
        return self.object1.object_id + " " + self.object2.object_id + ":" + self.label+":"+str(self.weight)

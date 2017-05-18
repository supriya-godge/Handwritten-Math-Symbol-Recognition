import math
import numpy as np

# This class is created to store the information about the symbol
class symbols:
    __slots__ = "stokes","name","boudingBox","boundingCenter"

    def __init__(self,strokes,name):
        self.stokes = strokes
        self.name =name
        self.boudingBox = self.find_bounding_box(self.stokes)
        self.boundingCenter = self.find_bounding_center(self.boudingBox)


    def find_bounding_box(self,strokes):
        new_list = self.convert_list(strokes)
        minX = np.min(new_list[:, 0])
        maxX = np.max(new_list[:, 0])
        minY = np.min(new_list[:, 1])
        maxY = np.max(new_list[:, 1])
        return [minX,maxX,minY,maxY]

    def find_bounding_center(self,boundBox):
        return [math.fabs(boundBox[0]-boundBox[1])/2, math.fabs(boundBox[2]-boundBox[3])/2]

    # To convert the list from 3D to 2D
    def convert_list(self,strokes):
        new_list=[]
        for alist in strokes:
            new_list+=alist
        return np.asarray(new_list)

#To create the feature matrix
def feature_extractor(all_inkml, training=False):
    for inkml in all_inkml:
        all_symbols=[]
        for obj in inkml.objects:
            trace=[]
            for trace_id in obj.trace_ids:
                trace.append(inkml.strokes[trace_id])
            all_symbols.append(symbols(trace,obj.label))

        index=0
        #It will find the n nearest symbols and create a feature vector for
        # a current symbol to all its nearest symbols.
        for obj in inkml.objects:
            clostest_symbol = find_nearest(obj,all_symbols[index+1:],2)
            for close_symb in clostest_symbol:
                create_feature(obj,close_symb)
            index+=1

def create_feature(symbol1,symbol2):
    pass


def find_nearest(item,all_symbols, total):
    distances = find_distance(item,all_symbols)
    indices=np.asarray(distances).argsort()[:total]
    nearest_symbol=[]
    for indi in indices:
        nearest_symbol.append(all_symbols[indi])
    return nearest_symbol


def distance(point1,point2):
    p1=np.asarray(point1)
    p2=np.asarray(point2)
    return np.sqrt(np.sum((p1-p2)**2))


def find_distance(item, all_symbols):
    distances = []
    for current_point in all_symbols:
        distances.append(distance(item,current_point))
    return distances
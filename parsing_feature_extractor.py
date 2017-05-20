"""
Modules for feature extraction for parsing

@author: Ajinkya Dhaigude (ad8454@rit.edu)
@author: Supriya Godge (spg5835@rit.edu)
"""

import math
import numpy as np


def bounding_box(strokes):
    new_list = convert_list(strokes)
    minX = np.min(new_list[:, 0])
    maxX = np.max(new_list[:, 0])
    minY = np.min(new_list[:, 1])
    maxY = np.max(new_list[:, 1])
    return [minX,maxX,minY,maxY]

def bounding_box_center(boundBox):
    return [math.fabs(boundBox[0]-boundBox[1])/2, math.fabs(boundBox[2]-boundBox[3])/2]

    # To convert the list from 3D to 2D
def convert_list(strokes):
    new_list=[]
    for alist in strokes:
        new_list+=alist
    return np.asarray(new_list)

#To create the feature matrix
def feature_extractor(all_inkml, training=False):
    for inkml in all_inkml:
        index=0
        #It will find the n nearest symbols and create a feature vector for
        # a current symbol to all its nearest symbols.
        if training:
            train_parser(inkml)
            continue
        for obj in inkml.objects:
            clostest_symbol = find_nearest(obj,inkml.objects[index+1:],2)
            for close_symb in clostest_symbol:
                create_feature(obj,close_symb)
            index+=1

def train_parser(inkml):
    for relation in inkml.relations:
        pass

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

def feature_vertical_distance_between_boundingcenter(symb1,symb2):
    s1_center= symb1.boundingCenter
    s2_center= symb2.boundingCenter
    return [s1_center[1]-s2_center[1]]

def feature_distance_between_bounding_center(symb1,symb2):
    return list(distance(symb1.boundingCenter,symb2.boundingCenter))


def feature_writing_slop(strok1,strok2):
    s1=strok1[len(strok1)-1]
    s2=strok2[0]
    return [math.atan2(s2[1]-s1[1],s2[0]-s1[0])]

def feature_PSC(symb1,symb2,all_other_symb):
    feature_vector=[]
    boundingBox = bounding_box(symb1+symb2)
    center = bounding_box_center(boundingBox)
    radius = boundingBox[0] if boundingBox[0]>boundingBox[1] else boundingBox[1]
    bounding_circle = (center,radius)
    feature_vector += calculate_strok(bounding_circle,symb1)[1]
    feature_vector += calculate_strok(bounding_circle,symb2)[1]
    feature_vector += calculate_strok(bounding_circle,all_other_symb)[1]
    return feature_vector



def calculate_strok(bounding_circle,symb):
    bins = np.zeros((6,5))
    radius = bounding_circle[1]
    ang_round=60
    rad_round=radius/5
    count=1
    center = bounding_circle[0]
    symb = convert_list(symb)
    for s1 in symb:
        angle=math.atan2(center[1] - s1[1], center[0] - s1[0])
        angle = math.degrees(angle+360)%360
        angle=round(angle*ang_round)//ang_round
        dist = round(distance(center,s1)*rad_round)/rad_round
        if dist < radius:
            count+=1
            d=int(round(dist/rad_round))
            a=angle//ang_round
            if a==6:
                a=5
            bins[a][d-1]+=1
    return list(bins.flatten()), list(bins.flatten()/count)
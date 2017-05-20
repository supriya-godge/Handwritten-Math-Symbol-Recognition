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


def feature_extractor(all_inkml, training=False):
    feature_matrix = []
    GT = []

    if training:
        for inkml in all_inkml:
            for relation in inkml.relations:
                feature_matrix.append(create_feature(relation.object1, relation.object2, inkml.objects))
                GT.append(relation.label)

        return np.asarray(feature_matrix), np.asarray(GT)

    else:
        for inkml in all_inkml:
            for index, obj in enumerate(inkml.objects):
                if len(inkml.objects) > index+1:
                    next_obj = inkml.objects[index+1]
                    feature_matrix.append(create_feature(obj, next_obj, inkml.objects))

                # It will find the n nearest symbols and create a feature vector for
                # a current symbol to all its nearest symbols.
                #closest_symbols = find_nearest(obj, inkml.objects[index + 1:], 2)
                #for close_symb in closest_symbols:
                #    create_feature(obj,close_symb)
        return np.asarray(feature_matrix)


def create_feature(symbol1,symbol2,all_symb):
    feature_functions = [feature_vertical_distance_between_boundingcenter,
                         feature_horizontal_distance_between_boundingcenter,
                         feature_corner_angle_with_center,
                         feature_distance_between_bounding_center,
                         feature_angle_bounding_center,
                         feature_vertical_offset,
                         feature_writing_slop]

    # TODO: feature_PSC

    feature_vector=[]

    for func in feature_functions:
        feature_vector += (func(symbol1,symbol2))

    other_symb = all_symb[:]
    other_symb.remove(symbol1)
    other_symb.remove(symbol2)


    if len(other_symb) > 0:
        other_symb = [symb.strokes for symb in other_symb][0]
    else:
        other_symb = [[]]

    feature_vector += (feature_PSC(symbol1, symbol2,other_symb))
    return feature_vector



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

def manhatten_distance(sym1,sym2):
    dist = sym1.boundingCenter[0]-sym2.boundingCenter[0]+sym1.boundingCenter[1]-sym2.boundingCenter[1]
    return dist

def find_distance(item, all_symbols):
    distances = []
    for current_point in all_symbols:
        distances.append(manhatten_distance(item,current_point))
    return distances

def feature_vertical_distance_between_boundingcenter(symb1,symb2):
    s1_center= symb1.boundingCenter
    s2_center= symb2.boundingCenter
    return [s1_center[0]-s2_center[0]]

def feature_vertical_offset(symb1, symb2):
    s1 = symb1.boundingBox
    s2 = symb2.boundingBox
    return [s1[3] - s2[3],s1[3] - s2[2]]

def feature_horizontal_distance_between_boundingcenter(symb1,symb2):
    s1_center= symb1.boundingCenter
    s2_center= symb2.boundingCenter
    return [s1_center[1]-s2_center[1]]

def feature_corner_angle_with_center(symb1,symb2):
    angle_list = []
    angle_list.append(angle_between_two_points([symb1.boundingBox[0],symb1.boundingBox[2]],symb2.boundingCenter))
    angle_list.append(angle_between_two_points([symb1.boundingBox[1], symb1.boundingBox[2]], symb2.boundingCenter))
    angle_list.append(angle_between_two_points([symb1.boundingBox[0], symb1.boundingBox[3]], symb2.boundingCenter))
    angle_list.append(angle_between_two_points([symb1.boundingBox[1], symb1.boundingBox[3]], symb2.boundingCenter))
    return angle_list

def angle_between_two_points(point1,point2):
    co = np.dot(point1,point2)
    sin = np.linalg.norm(np.cross(point1,point2))
    angle = np.arctan2(co, sin)
    angle = round_angle(angle,30)
    return angle



def feature_distance_between_bounding_center(symb1,symb2):
    return [distance(symb1.boundingCenter,symb2.boundingCenter)]


def feature_writing_slop(sym1,sym2):
    s1=sym1.strokes[-1][-1]
    s2=sym2.strokes[0][0]
    angle = math.atan2(s2[1]-s1[1],s2[0]-s1[0])
    angle = round_angle(angle,30)
    return [angle]

def round_angle(angle,rnd):
    angle = math.degrees(angle + 360) % 360
    angle = round(angle * rnd) // rnd
    return angle


def feature_angle_bounding_center(symb1,symb2):
    s1= symb1.boundingCenter
    s2= symb2.boundingCenter
    angle = math.atan2(s2[1] - s1[1], s2[0] - s1[0])
    angle = round_angle(angle, 30)
    return [angle]




def feature_PSC(symb1,symb2,all_other_symb):
    feature_vector=[]
    boundingBox = bounding_box(symb1.strokes+symb2.strokes)
    center = bounding_box_center(boundingBox)
    radius = boundingBox[0] if boundingBox[0]>boundingBox[1] else boundingBox[1]
    bounding_circle = (center,radius)
    feature_vector += calculate_strok(bounding_circle, symb1.strokes)[1]
    feature_vector += calculate_strok(bounding_circle, symb2.strokes)[1]
    feature_vector += calculate_strok(bounding_circle, all_other_symb)[1]
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
        angle = round_angle(angle,ang_round)
        dist = round(distance(center,s1)*rad_round)/rad_round
        if dist < radius:
            count+=1
            d=int(round(dist/rad_round))
            a=angle//ang_round
            if a==6:
                a=5
            bins[a][d-1]+=1
    return list(bins.flatten()), list(bins.flatten()/count)
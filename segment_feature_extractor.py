import numpy as np
from pattern_rec_utils import *
import math
import numpy as np

def rough_trial(all_inkml):
    """
    Temporary.
    Segments each stroke as a new symbol
    :param all_inkml:
    :return:
    """
    for inkml in all_inkml:
        for trace_id in inkml.strokes.keys():
            inkml.create_object([trace_id])


def feature_extractor(all_inkml):
    """
    Temporary.
    Segments each stroke as a new symbol
    :param all_inkml:
    :return:
    """
    feature_method=[feature_min_distance_betw_strockes,\
                    feature_horizontal_overlapping_of_surrounding_rectangles,\
                    feature_distance_horizontal_offset_startandEnd_position,\
                    feature_distance_vertical_offset_startandEnd_position,\
                    feature_backward_moment,\
                    feature_parallelity_of_stroks,\
                    feature_distance_between_bounding_center,\
                    feature_distance_average_center,\
                    feature_maximal_point_pair_distance,\
                    feature_horizntal_offset_strok1EndPoint_stroke2StartPoint,\
                    feature_vertical_distance_between_boundingcenter,\
                    feature_writing_slop]

    feature_matrix = []
    truth_labels = []

    # to track progress
    total = len(all_inkml)
    prev = 0
    done = 0

    for inkml in all_inkml:
        keys = list(inkml.strokes.keys())

        for index in range(len(keys) - 1):
            strok1 = inkml.strokes[keys[index]]
            strok2 = inkml.strokes[keys[index + 1]]
            AllOtherStroks = get_all_other_strocks([index, index + 1], inkml)
            feature_vector = []
            should_merge = False

            for func in feature_method:
                feature = func(strok1, strok2)
                feature_vector += feature

            bb = bounding_box(strok1+strok2)
            width = bb[1]-bb[0] if bb[1]-bb[0]!=0 else 1
            feature_vector[:] = [x / width for x in feature_vector]
            feature = feature_PSC(strok1,strok2,AllOtherStroks)
            feature_vector += feature

            for obj in inkml.objects:
                if keys[index] in obj.trace_ids and keys[index+1] in obj.trace_ids:
                    should_merge = True

            feature_matrix.append(feature_vector)
            truth_labels.append(should_merge)

        # to track progress
        done += 1
        track = int((done / total) * 100)
        if track % 10 == 0 and track != prev:
            prev = track
            print('{}% done'.format(track))

    feature_matrix = np.asarray(feature_matrix)
    truth_labels = np.asarray(truth_labels)

    return feature_matrix, truth_labels


def get_all_other_strocks(strokes, inkml):
    all_other=[]
    for key in inkml.strokes.keys():
        if key not in strokes:
            all_other += inkml.strokes[key]
    return all_other




def bounding_box(strok):
    '''
    :param strok:
    :return:mininum X, Maximum X,mininum Y, Maximum Y
    '''
    minX,maxX,minY,maxY=get_Min_Max(strok)
    return [minX,maxX,minY,maxY]

def get_Min_Max(stroke1):
    if not isinstance(stroke1[0],list):
        return stroke1[0],stroke1[0],stroke1[1],stroke1[1]
    temp = np.asarray(stroke1)
    min_x = np.min(temp[:,0])
    min_y = np.min(temp[:,1])
    max_x = np.max(temp[:,0])
    max_y = np.max(temp[:,1])

    return min_x,max_x,min_y,max_y


def feature_min_distance_betw_strockes(strok1,strok2):
    s1=get_Min_Max(strok1)
    s2=get_Min_Max(strok2)

    if s1[1]<s2[0]:
        return [0]
    else:
        return [s2[0]-s1[1]]

def feature_horizontal_overlapping_of_surrounding_rectangles(strok1,strok2):
    s1=get_Min_Max(strok1)
    s2=get_Min_Max(strok2)
    if s1[1]<s2[0]:
        return [s2[0] - s1[1]]
    else:
        return [0]

def feature_distance_horizontal_offset_startandEnd_position(strok1,strok2):
    l = len(strok1)-1
    l1=len(strok2)-1
    return [distance(strok1[0],strok2[0]),\
            strok1[0][0]-strok2[0][0], \
           distance(strok1[l], strok2[l1]), \
           strok1[l][0] - strok2[l1][0]]


def feature_distance_vertical_offset_startandEnd_position(strok1,strok2):
    l = len(strok1)-1
    l1=len(strok2)-1
    return [distance(strok1[0],strok2[0]),\
            strok1[0][0]-strok2[0][0], \
           distance(strok1[l], strok2[l1]), \
           strok1[l][0] - strok2[l1][0]]

def feature_backward_moment(strok1,strok2):
    l1=len(strok2)-1
    return [distance(strok1[0],strok2[l1])]



def distance(point1,point2):
    p1=np.asarray(point1)
    p2=np.asarray(point2)
    return np.sqrt(np.sum((p1-p2)**2))

def feature_parallelity_of_stroks(strok1,strok2):
    '''
    v1=[start point][end point] for strok1
    v2=[start point][end point] for strok2
    \theta = \fract{cos(v1.v2)}{|v1.v2|}
    :return:
    '''
    v1=np.array([strok1[0],strok1[len(strok1)-1]])
    v2 = np.array([strok2[0], strok2[len(strok2)-1]])
    co = np.dot(v1,v2)
    sin = np.linalg.norm(np.cross(v1,v2))
    return list(np.arctan2(co,sin).flatten())


def feature_distance_between_bounding_center(strok1,strok2):
    s1_center= np.asarray(bounding_box_center(strok1))
    s2_center = np.asarray(bounding_box_center(strok2))
    return list(s1_center-s2_center)

def feature_distance_average_center(strok1,strok2):
    s1 = np.asarray(strok1)
    s2 = np.asarray(strok2)
    s1_center = np.array([np.sum(s1[:, 0]) / s1.shape[0], np.sum(s1[:, 1]) / s1.shape[0]])
    s2_center = np.array([np.sum(s2[:, 0]) / s2.shape[0], np.sum(s2[:, 1]) / s2.shape[0]])
    return list(s1_center-s2_center)

def bounding_box_center(strok1):
    s1=get_Min_Max(strok1)
    s1_center = np.array([math.fabs(s1[0]-s1[1])/2,math.fabs(s1[2]-s1[3])/2])
    return s1_center

def feature_maximal_point_pair_distance(strok1,strok2):
    s1=get_Min_Max(strok1)
    s2=get_Min_Max(strok2)
    return [s1[0]-s2[1]]

def feature_horizntal_offset_strok1EndPoint_stroke2StartPoint(strok1,strok2):
    l = len(strok1)-1
    return [strok1[l][0] - strok2[0][0]]


def feature_vertical_distance_between_boundingcenter(strok1,strok2):
    s1_center=bounding_box_center(strok1)
    s2_center=bounding_box_center(strok2)
    return [s1_center[1]-s2_center[1]]

def feature_writing_slop(strok1,strok2):
    s1=strok1[len(strok1)-1]
    s2=strok2[0]
    return [math.atan2(s2[1]-s1[1],s2[0]-s1[0])]

def feature_PSC(strok1,strok2,all_other_strok):
    feature_vector=[]
    boundingBox = bounding_box(strok1+strok2)
    center = bounding_box_center(strok1+strok2)
    radius = boundingBox[0] if boundingBox[0]>boundingBox[1] else boundingBox[1]
    bounding_circle = (center,radius)
    feature_vector += calculate_strok(bounding_circle,strok1)[1]
    feature_vector += calculate_strok(bounding_circle,strok2)[1]
    feature_vector += calculate_strok(bounding_circle,all_other_strok)[1]
    return feature_vector



def calculate_strok(bounding_circle,strok1):

    bins = np.zeros((6,5))
    radius = bounding_circle[1]
    ang_round=60
    rad_round=radius/5
    count=1
    center = bounding_circle[0]
    for s1 in strok1:
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


















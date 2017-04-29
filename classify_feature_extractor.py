"""
Modules for feature extraction for classification

@author: Ajinkya Dhaigude (ad8454@rit.edu)
@author: Supriya Godge (spg5835@rit.edu)
"""

import collections
import numpy as np
import cv2
import math

global max_coord

def get_training_matrix(all_inkml, local_max_coord, functions_online, functions_offline):
    """
    Get a matrix with feature vectors for training.
    Each feature vector list has a label as the last element

    :param all_inkml: list of Inkml objects
    :param local_max_coord: width of square image for offline features
    :param functions_online: list of function names to call
    :param functions_offline: list of function names to call
    :return: a list of feature vectors, a list of ground truth labels
    """

    # set global variable
    global max_coord
    max_coord = local_max_coord

    feature_matrix = []
    truth_labels = []

    # to track progress
    total = len(all_inkml)
    done = 0

    for inkml in all_inkml:
        for obj in inkml.objects:
            feature_vector = []

            obj_coords, obj_image = get_online_offline_data(inkml, obj)

            for function in functions_online:
                feature = function(obj_coords)
                feature_vector += feature

            for function in functions_offline:
                feature = function(obj_image)
                feature_vector += feature

            truth_labels.append(obj.label)
            feature_matrix.append(feature_vector)

        # to track progress
        done += 1
        track = ((done/total)*100)
        if track % 10 == 0:
            print('{}% done'.format(track))

    feature_matrix = np.asarray(feature_matrix)
    truth_labels = np.asarray(truth_labels)

    return feature_matrix, truth_labels


def get_online_offline_data(inkml, obj):
    """
    Get the online and offline data points. Online data points
    are the scaled coordinates and offline datapoints are an image.

    :param inkml: Inkml object
    :param obj: SymbolObject object
    :return: (list, cv2 image)
    """

    obj_coords = []  # for online features
    # max-coord + 1 because sometimes the very edge pixels would get clipped
    obj_image = np.zeros((max_coord+1, max_coord+1), np.uint8)  # for offline features

    # get the coordinates and add to list. Also draw on cv2 image
    for trace_id in obj.trace_ids:
        coords = np.asarray(inkml.strokes[trace_id], np.int32)
        obj_coords.append(coords)
        coords = coords.reshape((-1, 1, 2))
        cv2.polylines(obj_image, [coords], False, 255)

    # center the image by finding the bounding rect around
    # the symbol and centering it
    x, y, w, h = cv2.boundingRect(obj_image)

    # center of the bounding box
    mid_x, mid_y = (x + w) // 2, (y + h) // 2
    mid = max_coord // 2
    # translation in x and y direction
    tx, ty = abs(mid - mid_x), abs(mid - mid_y)
    # translate symbol to image center
    m = np.float32([[1, 0, tx], [0, 1, ty]])
    obj_image = cv2.warpAffine(obj_image, m, (max_coord+1, max_coord+1))

    # apply morphological transformations
    obj_image = cv2.dilate(obj_image, (3, 3), iterations=1)
    obj_image = cv2.GaussianBlur(obj_image, (3, 3), 1)

    # display the image
    #display_image(obj_image)

    return obj_coords, obj_image


def display_image(img):
    cv2.namedWindow('window', cv2.WINDOW_NORMAL)
    cv2.imshow('window', img)
    cv2.resizeWindow('window', 600, 600)
    cv2.waitKey(0)


def XaxisProjection(img):
    projection=[]
    for iter in range(max_coord):
        projection.append(np.sum(img[:, iter]))
    return projection

def YaxisProjection(img):
    projection=[]
    for iter in range(0, max_coord):
        projection.append(np.sum(img[iter]))
    return projection

def DiagonalProjections(img):
    # create initial projection arrays initialzed to zeroes
    projectionTopLeft = [0]*(max_coord *2 - 1)
    projectionTopRight = [0] * (max_coord * 2 - 1)
    for i in range(0, max_coord):
        for j in range(0, max_coord):
            # add to TopLeft if index sums match
            projectionTopLeft[i+j] += img[i, j]
            # reverse the index of column and then add if index sums match
            idY = max_coord - j - 1
            projectionTopRight[i + idY] += img[i, j]

    # merge both diagonal features and return
    projectionTopLeft.extend(projectionTopRight)
    return projectionTopLeft

def zoning(img, numberOfbins=10):
    size = max_coord // numberOfbins
    prevY = 0
    zone=[]
    for iter in range(size, max_coord, size):
        prevX = 0
        #row=[]
        for jiter in range(size, max_coord, size):
            part = img[prevY:iter, prevX:jiter]
            zone.append(np.sum(part)/(size*size))
        #zonning.append(row)
    return zone

def OnlineFeature(strock):
    #print(strock)
    first=strock[0][0]
    #print(first)
    last = strock[len(strock)-1][len(strock[len(strock)-1])-1]
    ans = (first[0]-last[0])**2+(first[1]-last[1])**2
    return [math.sqrt(ans)]

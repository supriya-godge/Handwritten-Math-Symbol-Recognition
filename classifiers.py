import sklearn
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
import numpy

#class Classifiers:
def random_forest_train(train_features, ground_labels):
    print("rf = RandomForestClassifier(n_estimators=10, max_depth=None, min_samples_split=2, random_state=0) with biase")
    rf = RandomForestClassifier(n_estimators=10, max_depth=None, min_samples_split=2, random_state=0)
    rf = rf.fit(train_features, ground_labels)
    return rf

def random_forest_test(rf, test_features):
    score=0
    prediction = rf.predict(test_features)

    '''
    for index in range(len(test_labels)):
        classPredict = prediction[index]
        #print(classPredict," ",test_labels[index])
        if classPredict == test_labels[index]:
            score+=1
        else:
            print(test_labels[index]," ",classPredict)

    print('Random Forest score correct: ', score)
    print('Random Forest incorrect: ', len(test_labels) - score)
    print('Accuracy:',(score/len(test_labels)*100))
    '''

    return prediction

def kd_tree_train(train_features):
    kd = sklearn.neighbors.KDTree(train_features)
    return kd

def kd_tree_test(kd, test_features, test_labels, ground_labels):
    score = 0
    label_idx=0

    #results = []
    dist, indices = kd.query(test_features, k=1)

    # if ground_labels is not None:
    #     for feature in test_features:
    #         dist, ind = kd.query(feature.reshape(1, -1), k=1)
    #         index = ind[label_idx][0]
    #         if ground_labels[index] == test_labels[label_idx]:
    #             score += 1
    #         label_idx+=1
    #     #dist, ind = kd.query(test_features, k=1)
    #     print('kdtree score correct: ', score)
    #     print('kdtree score incorrect: ', len(test_features) - score)
    #     print('kdtree accuracy: ',(score/len(test_features)*100))

    indices = [ele[0] for ele in indices]
    return indices
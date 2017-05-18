import sklearn
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier


def random_forest_train(train_features, ground_labels):
    print('Training Classifier...')
    rf = RandomForestClassifier(n_estimators=100, max_depth=None, min_samples_split=2, random_state=0)
    rf = rf.fit(train_features, ground_labels)
    return rf


def random_forest_test(rf, test_features):
    prediction = rf.predict(test_features)
    return prediction


def kd_tree_train(train_features):
    kd = sklearn.neighbors.KDTree(train_features)
    return kd


def kd_tree_test(kd, test_features):
    dist, indices = kd.query(test_features, k=1)
    indices = [ele[0] for ele in indices]
    return indices

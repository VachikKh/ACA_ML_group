from decision_tree import DecisionTree
from collections import defaultdict
import numpy as np

class RandomForest(object):
    """
    RandomForest a class, that represents Random Forests.

    :param num_trees: Number of trees in the random forest
    :param max_tree_depth: maximum depth for each of the trees in the forest.
    :param ratio_per_tree: ratio of points to use to train each of
        the trees.
    """
    def __init__(self, num_trees, max_tree_depth, ratio_per_tree=0.5):
        self.num_trees = num_trees
        self.max_tree_depth = max_tree_depth
        self.ratio_per_tree=ratio_per_tree
        self.trees = None

    def fit(self, X, Y):
        """
        :param X: 2 dimensional python list or numpy 2 dimensional array
        :param Y: 1 dimensional python list or numpy 1 dimensional array
        """
        self.trees = []
        for _ in range(self.num_trees):
            indices=np.arange(Y.shape[0])
            np.random.shuffle(indices)
            X=X[indices]
            Y=Y[indices]
            test_len=int(self.ratio_per_tree*len(X))
            X_train=X[:test_len]
            Y_train=Y[:test_len]
            tree=DecisionTree(self.max_tree_depth)
            tree.fit(X_train,Y_train)
            self.trees.append(tree)

    def predict(self, X):
        """
        :param X: 2 dimensional python list or numpy 2 dimensional array
        :return: (Y, conf), tuple with Y being 1 dimension python
        list with labels, and conf being 1 dimensional list with
        confidences for each of the labels.
        """
        predicts=[tree.predict(X) for tree in self.trees]
        predicts=[[predicts[i][j] for i in range(len(predicts))] for j in range(len(predicts[0]))]
        Y=[]
        conf=[]
        for r in predicts:
            results = defaultdict(np.float64)
            count=0
            for key in r:
                results[key]+=1
                count+=1
            Y.append(max(results,key=results.get))
            conf.append(results[Y[-1]]/count)
        return (Y, conf)

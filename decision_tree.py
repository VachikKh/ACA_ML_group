import numpy as np
import dtOmitted as dt
class DecisionTree(object):
    """
    DecisionTree class, that represents one Decision Tree

    :param max_tree_depth: maximum depth for this tree.
    """
    def __init__(self, max_tree_depth):
        self.max_depth = max_tree_depth

    def fit(self, X, Y):
        """
        :param X: 2 dimensional python list or numpy 2 dimensional array
        :param Y: 1 dimensional python list or numpy 1 dimensional array
        """
        if type(X) is np.ndarray:
            X=X.tolist()
        if type(Y) is np.ndarray:
            Y=Y.tolist()

        data=[X[i]+[Y[i]] for i in range(len(X))]
        
        self.root=dt.build_tree(data,max_depth=self.max_depth)


    def predict(self, X):
        """
        :param X: 2 dimensional python list or numpy 2 dimensional array
        :return: Y - 1 dimension python list with labels
        """
        Y=[]
        for x in X:
            tree=self.trees
            while not tree.is_leaf:
                if x[tree.column] < tree.value:
                    tree=tree.false_branch
                else:
                    tree=tree.true_branch
            Y.append(max(tree.current_results,key=tree.current_results.get))
        return Y
    

import matplotlib.pyplot as plt
import numpy as np

from decision_tree import DecisionTree
from random_forest import RandomForest
from logistic import logistic

def accuracy_score(Y_true, Y_predict):
    c = 0.
    for i in range(len(Y_true)):
        if Y_true[i] == Y_predict[i]:
            c += 1
    return c / len(Y_true)


def evaluate_performance():
    '''
    Evaluate the performance of decision trees and logistic regression,
    average over 1,000 trials of 10-fold cross validation

    Return:
      a matrix giving the performance that will contain the following entries:
      stats[0,0] = mean accuracy of decision tree
      stats[0,1] = std deviation of decision tree accuracy
      stats[1,0] = mean accuracy of logistic regression
      stats[1,1] = std deviation of logistic regression accuracy

    ** Note that your implementation must follow this API**
    '''

    # Load Data
    stats = np.zeros((3, 2))
    filename = 'SPECTF.dat'
    data = np.loadtxt(filename, delimiter=',')
    X = data[:, 1:]
    y = np.array([data[:, 0]]).T
    n, d = X.shape
    num_folds = 10
    num_trials = 50
    all_accuracies = []
    rf_all_accuracies = []
    l_all_accuracies = []
    for trial in range(num_trials):
        idx = np.arange(n)
        np.random.seed(13)
        np.random.shuffle(idx)
        X = X[idx]
        y = y[idx]

        Xtrain = X[:n - n // num_folds, :]  # train on first 100 instances
        Xtest = X[n - n // num_folds:, :]
        ytrain = y[:n - n // num_folds, :]  # test on remaining instances
        ytest = y[n - n // num_folds:, :]

        # train the decision tree
        classifier = DecisionTree(5)
        classifier.fit(Xtrain, ytrain)
        # output predictions on the remaining data
        y_pred = classifier.predict(Xtest)
        accuracy = accuracy_score(ytest, y_pred)
        all_accuracies.append(accuracy)

        rf_classifier = RandomForest(5, 100, 0.3)
        rf_classifier.fit(Xtrain, ytrain)
        rf_y_pred = rf_classifier.predict(Xtest)[0]
        rf_accuracy = accuracy_score(ytest, rf_y_pred)
        rf_all_accuracies.append(rf_accuracy)

        l_classifier = logistic()
        l_classifier.fit(Xtest, ytest)

        l_y_pred = l_classifier.predict(Xtest)
        l_accuracy = accuracy_score(ytest, l_y_pred)
        l_all_accuracies.append(l_accuracy)
        print('iter num :{0}'.format(trial))

        meanDecisionTreeAccuracy = np.mean(all_accuracies)
        stddevDecisionTreeAccuracy = np.std(all_accuracies)
        meanLogisticRegressionAccuracy = np.mean(l_all_accuracies)
        stddevLogisticRegressionAccuracy = np.std(l_all_accuracies)
        meanRandomForestAccuracy = np.mean(rf_all_accuracies)
        stddevRandomForestAccuracy = np.std(rf_all_accuracies)

        stats[0, 0] = meanDecisionTreeAccuracy
        stats[0, 1] = stddevDecisionTreeAccuracy
        stats[1, 0] = meanRandomForestAccuracy
        stats[1, 1] = stddevRandomForestAccuracy
        stats[2, 0] = meanLogisticRegressionAccuracy
        stats[2, 1] = stddevLogisticRegressionAccuracy

        print ("\tDecision Tree Accuracy = ", stats[0, 0], " (", stats[0, 1], ")")
        print ("\tRandom Forest Tree Accuracy = ", stats[1, 0], " (", stats[1, 1], ")")
        print ("\tLogistic Reg. Accuracy = ", stats[2, 0], " (", stats[2, 1], ")")

    # compute the training accuracy of the model
    meanDecisionTreeAccuracy = np.mean(all_accuracies)

    stddevDecisionTreeAccuracy = np.std(all_accuracies)
    meanLogisticRegressionAccuracy = np.mean(l_all_accuracies)
    stddevLogisticRegressionAccuracy = np.std(l_all_accuracies)
    meanRandomForestAccuracy = np.mean(rf_all_accuracies)
    stddevRandomForestAccuracy = np.std(rf_all_accuracies)

    # make certain that the return value matches the API specification
    stats = np.zeros((3, 2))
    stats[0, 0] = meanDecisionTreeAccuracy
    stats[0, 1] = stddevDecisionTreeAccuracy
    stats[1, 0] = meanRandomForestAccuracy
    stats[1, 1] = stddevRandomForestAccuracy
    stats[2, 0] = meanLogisticRegressionAccuracy
    stats[2, 1] = stddevLogisticRegressionAccuracy
    return stats


# Do not modify from HERE...
def main():
    stats = evaluate_performance()
    print ("Decision Tree Accuracy = ", stats[0, 0], " (", stats[0, 1], ")")
    print ("Random Forest Tree Accuracy = ", stats[1, 0], " (", stats[1, 1], ")")
    print ("Logistic Reg. Accuracy = ", stats[2, 0], " (", stats[2, 1], ")")
# ...to HERE.
if __name__ == "__main__":
    main()
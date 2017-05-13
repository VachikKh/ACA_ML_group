import numpy as np


def sigmoid(s):
    return 1 - 1 / (1 + np.exp(s)) if abs(s) < 10 else 0 if s < 0 else 1


def normalized_gradient(X, Y,beta,l):
    """
    :param X: data matrix (2 dimensional np.array)
    :param Y: response variables (1 dimensional np.array)
    :param beta: value of beta (1 dimensional np.array)
    :param l: regularization parameter lambda
    :return: normalized gradient, i.e. gradient normalized according to data
    """
    gr = l * beta
    s = 0
    for i in range(X.shape[0]):
        s += X[i] * Y[i] * (1 - sigmoid(Y[i] * beta.T.dot(X[i])))
    gr -= s
    s = 0
    for i in range(X.shape[0]):
        s += Y[i] * (1 - sigmoid(Y[i] * beta.T.dot(X[i])))
    gr[0] -= s
    return gr / X.shape[0]


def gradient_descent(xx, yy,l,epsilon,max_steps,step_size,beta):
    """
    Implement gradient descent using full value of the gradient.
    :param X: data matrix (2 dimensional np.array)
    :param Y: response variables (1 dimensional np.array)
    :param l: regularization parameter lambda
    :param epsilon: approximation strength
    :param max_steps: maximum number of iterations before algorithm will
        terminate.
    :return: value of beta (1 dimensional np.array)
    """
    X = xx.copy()
    Y = yy.copy()
    gr = np.zeros(X.shape[1])

    v = np.var(X, axis=0, dtype=float) ** 0.5
    m = np.mean(X, axis=0, dtype=float)
    for i in range(1, X.shape[1]):
        for j in range(X.shape[0]):
            if v[i] != 0:
                X[j][i] -= m[i]
                X[j][i] /= v[i]
    l = np.array([l / v[_] ** 2 if v[_] != 0 else 0 for _ in range(X.shape[1])])

    for s in range(max_steps):
        old = beta.copy()
        gr = step_size * normalized_gradient(X, Y,beta,l)
        beta -= gr
        if ((beta - old) ** 2).sum() / ((beta ** 2).sum()) < epsilon ** 2:
            break
        pass
    for i in range(X.shape[1]):
        if i == 0:
            beta[0] = beta[0] - np.sum(
                np.array([m[i] * beta[i] / v[i] if v[i] != 0 else 0 for i in range(1, m.shape[0])]))
        else:
            beta[i] = beta[i] / v[i] if v[i] != 0 else 0
    return beta


class logistic(object):
    def __init__(self,epsilon=1e-6, l=1, step_size=1e-4, max_steps=1000):
        self.epsilon=epsilon
        self.step_size=step_size
        self.max_steps=max_steps
        self.l=l
    def fit(self,xx,yy):
        """
        :param xx: 2 dimensional python list or numpy 2 dimensional array
        :param yy: 1 dimensional python list or numpy 1 dimensional array
        """
        self.beta=np.random.normal(0,1,xx.shape[1])
        self.beta=gradient_descent(xx,yy,epsilon=self.epsilon,l=self.l,step_size=self.step_size,max_steps=self.max_steps,beta=self.beta)
    def predict(self,X):
        """
        :param X: 2 dimensional python list or numpy 2 dimensional array
        :return: (Y, conf), tuple with Y being 1 dimension python
        list with labels, and conf being 1 dimensional list with
        confidences for each of the labels.
        """
        return [1 if self.beta.dot(x)>0 else 0 for x in X]

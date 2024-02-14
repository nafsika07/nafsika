# -*- coding: utf-8 -*-
"""logistic_regression_cornell.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16l-87C3wqDaj6GmWkxlIGufONPDHGzVg

**CLASSIFICATION**
"""

import numpy as np
import pandas as pd
from sklearn import datasets
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

iris = datasets.load_iris(as_frame=True)
iris_X = iris.data
iris_y = iris.target
pd.concat([iris_X, iris_y], axis=1)

plt.rcParams['figure.figsize'] = [12, 4]
p1 = plt.scatter(iris_X.iloc[:, 0], iris_X.iloc[:, 1], c=iris_y, edgecolor='k', s=60, cmap=plt.cm.Paired)
plt.xlabel('Sepal length (cm)')
plt.ylabel('Sepal width (cm)')
plt.legend(handles=p1.legend_elements()[0], labels = ['Setosa', 'Versicolour', 'Virginica'], loc='lower right')

logreg = LogisticRegression(C=1e5)
X = iris_X.to_numpy()[:, :2]
Y = iris_y.copy()
logreg.fit(X,Y)

xx, yy = np.meshgrid(np.arange(4,8.2,0.02), np.arange(1.8,4.5,0.02))
# np.ravel() - return a contiguous flattened array
# np.c_() - translates sliced objects to concatenation along the second axis
Z = logreg.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)
# plt.pcolormesh(X,Y,C) - create a pseudocolor plot
#     C - the mesh data
plt.pcolormesh(xx, yy, Z, cmap=plt.cm.Paired)
plt.scatter(X[:,0], X[:,1], c=Y, edgecolor='k', s=60, cmap=plt.cm.Paired)
plt.xlabel('Sepal length (cm)')
plt.ylabel('Sepal width (cm)')

"""**LOGISTIC REGRESSION**"""

iris_y2 = iris_y.copy()
iris_y2[iris_y2 == 2] = 1
p1 = plt.scatter(iris_X.iloc[:, 0], iris_X.iloc[:, 1], c=iris_y2, edgecolor='k', s=60, cmap=plt.cm.Paired)
plt.xlabel('Sepal length (cm)')
plt.ylabel('Sepal width (cm)')
plt.legend(handles=p1.legend_elements()[0], labels=['Setosa', 'Non-Setosa'], loc='lower right')

def sigmoid(z):
  return 1 / (1 + np.exp(-z))

z = np.linspace(-5,5)
plt.plot(z, sigmoid(z))
plt.xlabel('z')
plt.ylabel('sigmoid(z)')

def f(X, theta):
  """ The sigmoid model we are trying to fit.
  """
  return sigmoid(X.dot(theta))

def log_likelihood(theta, X, y):
  """ The cost function defining the goodness of fit.
  """
  return (y*np.log(f(X, theta) + 1e-6) + (1-y)*np.log(1 - f(X, theta) + 1e-6)).mean()

def log_likelihood_gradient(theta, X, y):
  return np.mean((f(X, theta) - y) * X.T, axis=1)

threshold = 5e-5
step_size = 1e-1
theta, theta_prev = np.zeros((3,)), np.ones((3,))
opt_pts = [theta]
opt_grads = []
iter = 0

iris_X['one'] = 1
X_train = iris_X.iloc[:, [0, 1, -1]].to_numpy()
y_train = iris_y2.to_numpy()

while np.linalg.norm(theta - theta_prev) > threshold:
  if iter % 50000 == 0:
    print('Iteration %d. Log-likelihood: %.6f' % (iter, log_likelihood(theta, X_train, y_train)))
  theta_prev = theta
  gradient = log_likelihood_gradient(theta, X_train, y_train)
  theta = theta_prev - step_size*gradient
  opt_pts += [theta]
  opt_grads += [gradient]
  iter += 1

x_min = iris_X.iloc[:, 0].min() - 0.5
x_max = iris_X.iloc[:, 0].max() + 0.5
y_min = iris_X.iloc[:, 1].min() - 0.5
y_max = iris_X.iloc[:, 1].max() + 0.5

xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02), np.arange(y_min, y_max, 0.02))
Z = f(np.c_[xx.ravel(), yy.ravel(), np.ones(xx.ravel().shape)], theta)
Z[Z>0.5] = 1
Z[Z<0.5] = 0
Z = Z.reshape(xx.shape)
plt.pcolormesh(xx, yy, Z, cmap=plt.cm.Paired)
p1 = plt.scatter(iris_X.iloc[:,0], iris_X.iloc[:,1], c=iris_y2, edgecolor='k', s=60, cmap=plt.cm.Paired)
plt.xlabel('Sepal length (cm)')
plt.ylabel('Sepal width (cm)')
plt.legend(handles=p1.legend_elements()[0], labels=['Setosa', 'Non-Setosa'], loc='lower right')


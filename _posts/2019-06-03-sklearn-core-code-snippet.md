---
layout: post
title: Sklearn core code snippet
categories: [blog]
tags: [machine-learning]
---

Core code snippet for [scikit-learn](https://scikit-learn.org) machine learning applications using the [iris dataset](https://en.wikipedia.org/wiki/Iris_flower_data_set) and [k-Nearest Neighbor classifier](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm)

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


iris_dataset = load_iris()
# get the dataset using the load_iris function
#   type(iris_dataset) is sklearn.utils.Bunch, which is
#   similar to a Python dictionary e.g. iris_dataset.keys()


X_train, X_test, y_train, y_test = train_test_split( iris_dataset['data'], \
    iris_dataset['target'], random_state=0)
# by default 75% train, 25% test

knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(X_train, y_train)

score = knn.score(X_test, y_test)
# measures the accuracy i.e. the fraction of flowers
#   wherein the right species were predicted
#   same as:
#       y_pred = knn.predict(X_test)
#       np.mean(y_pred == y_test)

print(f"Model test set score: {score:.2f}")

```

<!--more-->

Applying model to new data, e.g.

```python
import numpy as np

# data must be of type: numpy.ndarray
X_new = np.array([[5, 2.9, 1, 0.2]])

prediction = knn.predict(X_new)

X_new_label = iris_dataset['target_names'][prediction]
print(f"Predicted name of new dataset: {X_new_label}")

```

#### Other notes
1. *k*-NN (or any algorithm that generates a predictive model) can be used to [detect anomalies in the data](https://algobeans.com/2016/09/14/k-nearest-neighbors-anomaly-detection-tutorial)
2. *k*-NN may not be a good choice for large datasets as the [algorithm](https://towardsdatascience.com/machine-learning-basics-with-the-k-nearest-neighbors-algorithm-6a6e71d01761) gets slower as the number of samples and/or independent variables increase. Moreover, it will not perform well on imbalanced datasets as the larger classes will overshadow the smaller classes (in which case, weighted voting instead of majority voting may be used to improve accuracy).

#### Reference:
Muller, A. C., Guido, S. (2017). *Introduction to machine learning with Python: A guide for data scientists*. Sebastopol, CA: O'Reilly Media Inc.

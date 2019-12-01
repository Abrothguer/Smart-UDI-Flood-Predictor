import pandas as pd
import numpy as np

from sklearn.svm import SVC

from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics


train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')

train.drop(['Nome'])
test.drop(['Nome'])

final = train['Final']
Xtrain, Xtest, Ytrain, Ytest = train_test_split(train, final, test_size=0.2, random_state=4)

knn = KNeighborsClassifier(n_neighbors = 5)
knn.fit(Xtrain, Ytrain)

pred = knn.predict(Xtest)
score = metrics.accuracy_score(Ytest, pred)

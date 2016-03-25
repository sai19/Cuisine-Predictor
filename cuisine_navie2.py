from __future__ import division
from collections import Counter
import operator
from sklearn import tree
from sklearn.preprocessing import LabelEncoder;
from sklearn.feature_extraction.text import CountVectorizer,HashingVectorizer,TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import svm
import pandas as pd
import numpy as np


data_total = pd.read_json("/media/sai/New Volume1/Practice/cuisine_predictor/train/train.json");
le = LabelEncoder();
cv = CountVectorizer(max_df=0.6);
train_data = data_total.head(int(0.9*len(data_total)));
test_data = data_total.tail(int(0.1*len(data_total)));
train_X = train_data['ingredients'];
train_X = [' '.join(v) for v in train_X];
train_Y = train_data['cuisine'];
train_X = cv.fit_transform(train_X).toarray();
train_Y = le.fit_transform(train_Y);
test_X = test_data['ingredients'];
test_X = [' '.join(v) for v in test_X];
test_X = cv.transform(test_X).toarray();
test_Y = le.transform(test_data['cuisine']);	

#tree_classifier = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0,max_depth=1, random_state=0)
#tree_classifier.fit(train_X, train_Y);
#Y = tree_classifier.predict(test_X);
svm_classifier = svm.LinearSVC(C=0.7);
svm_classifier.fit(train_X, train_Y);
Y = svm_classifier.predict(test_X);
print (1 - (np.count_nonzero(Y-test_Y)/len(Y)));


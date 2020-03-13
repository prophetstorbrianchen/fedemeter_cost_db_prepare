# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 17:49:44 2019

@author: Brian
"""

import sys
import os
import pandas as pd
import numpy as np
from pandas import DataFrame as df
from sklearn import cross_validation, ensemble, preprocessing, metrics
from sklearn.externals import joblib


def import_data():
    data = pd.read_csv("C:\\Users\\Brian\\Desktop\\fedemeter_data\\for_machine_learning_instance_family.csv")
    training_data = pd.DataFrame([data["cpu"], data["memory"]]).T
    testing_data = data["family"]

    print(training_data)
    print(testing_data)

    return training_data, testing_data


def training_model(training_data, testing_data):

    train_X, test_X, train_y, test_y = cross_validation.train_test_split(training_data, testing_data, test_size=0.1)

    forest = ensemble.RandomForestClassifier(n_estimators=100)
    forest_fit = forest.fit(train_X, train_y)

    # ----save model----
    print("SVM Model save...")
    joblib.dump(forest, "C:\\Users\\Brian\\Desktop\\fedemeter_data\\ml.pkl")
    forest = joblib.load("C:\\Users\\Brian\\Desktop\\fedemeter_data\\ml.pkl")

    test_y_predicted = forest.predict(test_X)

    accuracy = metrics.accuracy_score(test_y, test_y_predicted)
    print(accuracy)

    return forest


def prediction(cpu, memory):

    if os.path.isfile("C:\\Users\\Brian\\Desktop\\fedemeter_data\\ml.pkl"):
        print("檔案存在。")
        forest = joblib.load("C:\\Users\\Brian\\Desktop\\fedemeter_data\\ml.pkl")
    else:
        print("檔案不存在。")
        training_data, testing_data = import_data()
        forest = training_model(training_data, testing_data)

    x_data = pd.DataFrame([cpu, memory]).T
    family_type = forest.predict(x_data)

    if family_type == 0:
        print("General Purpose")
    elif family_type == 1:
        print("Compute Optimized")
    else:
        print("Memory Optimized")

    return family_type


if __name__ == '__main__':

    family_type = prediction(8, 64)
    print(family_type)



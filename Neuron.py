import csv

import numpy as np
from sklearn.linear_model import LinearRegression


def processing(data, name):
    Ox = []
    Oy = []
    with open(f'layouts/{name}/base.csv', 'r', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            Ox.append(row[:-1])
            Oy.append(row[-1])
    X = np.array(Ox)
    y = np.array(Oy)
    reg = LinearRegression().fit(X, y)
    proba = np.array([data])
    rez = int(reg.predict(proba))
    return rez if rez > 0 else 0

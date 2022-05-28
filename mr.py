from mrjob.job import MRJob
from mrjob.step import MRStep
import numpy as np
import pickle
from sklearn.neighbors import KNeighborsClassifier as KNC
import csv
import re


def open_pickle(filename):
    f = open(filename, 'rb')
    ob = pickle.load(f)
    f.close()
    return ob

KNN = [("five", open_pickle("5_neighbors_model.obj")), 
    ("ten", open_pickle("10_neighbors_model.obj")), 
    ("fifteen", open_pickle("15_neighbors_model.obj")),
    ("twenty", open_pickle("20_neighbors_model.obj"))]

class KNNSuccesses(MRJob):

    def mapper(self, _, line):
        try:
            var_list = [float(x) for x in line.strip().split(',')][1:]
            true_val = var_list[-1]
            if (0 > true_val > -1):
                true_val = 1
            elif (2 > true_val > 1):
                true_val = 2
            elif (4 > true_val > 3):
                true_val = 3
            elif (5 > true_val > 6):
                true_val = 4
            else:
                true_val = 1
            for model in KNN:
                yield model[0], model[1].score(np.array([var_list[0:-1]]), np.array([true_val]))
            yield "lines", 1
        except:
            yield 'h', 1

    def reducer(self, model, count):
        yield model, sum(count)


if __name__ == '__main__':
    KNNSuccesses.run()
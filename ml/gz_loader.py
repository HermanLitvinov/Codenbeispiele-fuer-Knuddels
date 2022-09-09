import gzip
import numpy
import pickle

#Klasse fuer Aenderung des Datasets in Listen und Rueckzug der Training und Test Data

def vectorize_output(x):
        vec = numpy.zeros((10, 1))
        vec[x] = 1.0
        return vec

class GZLoader():
    def __init__(self, path: str):
        self.path = path
        return

    def load_data(self):
        d = gzip.open(self.path, "rb")
        data = pickle._Unpickler(d)
        data.encoding = "latin1"
        tr_d, val_d, test_d = data.load()
        d.close()
        return (tr_d, test_d)

    def load_data_wrap(self):
        tr_d, test_d = self.load_data()

        tr_d_input = [numpy.reshape(x, (784, 1)) for x in tr_d[0]]
        tr_d_output = [vectorize_output(x) for x in tr_d[1]]
        tr_d_complete = list(zip(tr_d_input, tr_d_output))

        test_d_input = [numpy.reshape(x, (784, 1)) for x in test_d[0]]
        test_d_complete = list(zip(test_d_input, test_d[1]))

        return (tr_d_complete, test_d_complete)
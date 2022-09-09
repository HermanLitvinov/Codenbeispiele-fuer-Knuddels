#die neurale Netzwerk, die ist trainiert, um handgeschriebene Zahlen zu unterscheiden

import network
import gz_loader

#Verteilung des Datasets in Training Data und Test Data
tr_d, test_d = gz_loader.GZLoader("D:\programering\py\python\ml\data\mnist.pkl.gz").load_data_wrap()

#Training der Netzwerke und Praesentierung, wie viele Bilder aus Test Data erkannt wurde mit jeden Epoch
net = network.Network([784, 100, 10])
net.stochastic_gradient_descent(tr_d, 30, 10, 3.0, test_data = test_d)
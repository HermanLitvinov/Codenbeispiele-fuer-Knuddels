import numpy as np
import random

def sigmoid(z):
    return 1/(1+np.exp(-z))

def sigmoid_prime(z):
    return sigmoid(z)*(1-sigmoid(z))

class Network():
    def __init__(self, sizes):
        self.num_of_layers = len(sizes)
        self.weights = [np.random.randn(i, j) for i, j in zip(sizes[1:], sizes[:-1])]
        self.biases = [np.random.randn(i, 1) for i in sizes[1:]]

    def feedforward(self, x):
        a = x
        for w, b in zip(self.weights, self.biases):
            a = sigmoid(np.dot(w, a) + b)
        return a

    def stochastic_gradient_descent(self, training_data, minibatch_size, epochs, lr, test_data):
        for i in range(epochs):
            random.shuffle(training_data)
            minibatches = [training_data[j:j+minibatch_size] for j in range(0, len(training_data), minibatch_size)]
            for minibatch in minibatches:
                self.update_minibatch(minibatch, lr)

            print("Epoch {0}: {1}/{2}".format(i, self.evaluate(test_data), len(test_data)))
            

    def update_minibatch(self, minibatch, lr):
        d_weights = [np.zeros(w.shape) for w in self.weights]
        d_biases = [np.zeros(b.shape) for b in self.biases]

        for x, y in minibatch:
            d_weights1, d_biases1 = self.backpropagation(x, y)
            d_weights = [dw+dw1 for dw, dw1 in zip(d_weights, d_weights1)]
            d_biases = [db+db1 for db, db1 in zip(d_biases, d_biases1)]

        self.weights = [w - (lr/len(minibatch))*dw for w, dw in zip(self.weights, d_weights)]
        self.biases = [b - (lr/len(minibatch))*db for b, db in zip(self.biases, d_biases)]

    def backpropagation(self, x, y):
            dw = [np.zeros(w.shape) for w in self.weights]
            db = [np.zeros(b.shape) for b in self.biases]

            activation = x
            activations = [x]
            zs = []
            #feedforward
            for w, b in zip(self.weights, self.biases):
                z = np.dot(w, activation) + b
                activation = sigmoid(z)
                zs.append(z)
                activations.append(activation)

            #backprop
            delta = self.cost_derivative(activations[-1], y)*sigmoid_prime(zs[-1])
            dw[-1] = np.dot(delta, activations[-2].transpose())
            db[-1] = delta
            for l in range(2, self.num_of_layers):
                delta = np.dot(self.weights[-l+1].transpose(), delta) * sigmoid_prime(zs[-l])
                dw[-l] = np.dot(delta, activations[-l-1].transpose())
                db[-l] = delta
                
            return (dw, db)

    def cost_derivative(self, a, y):
        return (a-y)


    def evaluate(self, test_data):
        confirmed_data = [(np.argmax(self.feedforward(x)), y) for (x, y) in test_data]
        return sum(int(x == y) for (x, y) in confirmed_data)

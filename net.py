import math
import random
import string

class Net:
    def __init__(self, ni, nh, no):
        ni += 1 #bias node

        self.ni, self.nh, self.no = ni, nh, no

        self.wi = self.make_matrix(ni, nh)
        self.wo = self.make_matrix(nh, no)

        self.ai = [1.] * ni
        self.ah = [1.] * nh
        self.ao = [1.] * no

        # set them to random vaules
        for i in range(self.ni):
            for j in range(self.nh):
                self.wi[i][j] = self.rand(-0.2, 0.2)
        for j in range(self.nh):
            for k in range(self.no):
                self.wo[j][k] = self.rand(-2.0, 2.0)

        self.ci = self.make_matrix(ni, nh)
        self.co = self.make_matrix(nh, no)

    def rand(self, a, b):
        return (b-a)*random.random() + a

    def make_matrix(self, I, J, fill=0.):
        return [[fill for x in range(J)] for x in range(I)]

    def sigmoid(self, x):
        return math.tanh(x)

    def dsigmoid(self, y):
        return 1.0 - y**2

    def update(self, inputs):
        # input activations
        for i in range(self.ni-1):
            self.ai[i] = inputs[i]

        # hidden activations
        for j in range(self.nh):
            sum = 0.0
            for i in range(self.ni):
                sum += self.ai[i] * self.wi[i][j]
            self.ah[j] = self.sigmoid(sum)

        # output activations
        for k in range(self.no):
            sum = 0.0
            for j in range(self.nh):
                sum += self.ah[j] * self.wo[j][k]
            self.ao[k] = self.sigmoid(sum)

        return self.ao[:]


    def back_propagate(self, targets, N, M):
        # calculate error terms for output
        output_deltas = [0.0] * self.no
        for k in range(self.no):
            error = targets[k]-self.ao[k]
            output_deltas[k] = self.dsigmoid(self.ao[k]) * error

        # calculate error terms for hidden
        hidden_deltas = [0.0] * self.nh
        for j in range(self.nh):
            error = 0.0
            for k in range(self.no):
                error = error + output_deltas[k]*self.wo[j][k]
            hidden_deltas[j] = self.dsigmoid(self.ah[j]) * error

        # update output weights
        for j in range(self.nh):
            for k in range(self.no):
                change = output_deltas[k]*self.ah[j]
                self.wo[j][k] = self.wo[j][k] + N*change + M*self.co[j][k]
                self.co[j][k] = change

        # update input weights
        for i in range(self.ni):
            for j in range(self.nh):
                change = hidden_deltas[j]*self.ai[i]
                self.wi[i][j] = self.wi[i][j] + N*change + M*self.ci[i][j]
                self.ci[i][j] = change

        # calculate error
        error = 0.0
        for k in range(len(targets)):
            error = error + 0.5*(targets[k]-self.ao[k])**2
        return error


    def test(self, i):
        o = self.update(i)
        print(i, '->', o)
        return o

    def train(self, data, iterations=1000, N=0.5, M=0.1):
        # N: learning rate
        # M: momentum factor
        for i in range(iterations):
            error = 0.
            for inputs, outputs in data.items():
                self.update(inputs)
                error += self.back_propagate(outputs, N, M)
            #if i % 100 == 0:
            if True:
                print('error %-.5f' % error)

def demo():
    # Teach network XOR function
    data = {
        '00': '0',
        '01': '1',
        '10': '1',
        '11': '0'
    }

    process = lambda x: tuple(map(int,x))
    data = {process(k): process(v) for k, v in data.items()}

    # create a network with two input, two hidden, and one output nodes
    n = Net(2, 2, 1)
    # train it with some patterns
    n.train(data)
    # test it
    for i in data.keys():
        n.test(i)



if __name__ == '__main__':
    demo()

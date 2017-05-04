import numpy as np
from numpy import array
import os


#a sigmoid function

np.random.seed(1)

# creating weights or synapses between neural network

syn0 = 2 * np.random.random((6, 5)) - 1  # 3x4 matrix of weights and 1 as a bias
syn1 = 2 * np.random.random((5, 1)) - 1


def nonlin(x, deriv =False):
    if deriv == True:
        return (x*(1-x))
    return 1/(1+np.exp(-x))


def find(file,final,k):
        global syn0
        global syn1
        fp = open('featureinputinnet/testfeatures/'+file, 'r', encoding='utf-8')
        y = fp.read()
        y = y.strip()
        flist = []
        for i in y.split('\n'):
            list = []
            for j in i.split():
                list.append(j)
            lis = [float(k) for k in list]
            flist.append(lis)
        print(len(flist))

        x = array(flist)

        print(type(x))

        y = np.array(final)
        # y=np.array([[1],[1],[0],[0],[0],[1],[0],[0],[0],[0],[1],[1],[1],[0],[0],[1],[1],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[1],[1],[0],[0],[0],[0],[0],[0]])
        # seed
        print(type(y))


        # training

            # layers
        l0 = x
        l1 = nonlin(np.dot(l0, syn0))  # np.dot is matrix multiplication
        l2 = nonlin(np.dot(l1, syn1))

            # back proppogation
        l2_error = y - l2
        if k % 100 == 0:
            print("Error:" + str(np.mean(np.abs(l2_error))))
        l2_delta = l2_error * nonlin(l2, deriv=True)  # the difference in the quantities at each layer
        l1_error = l2_delta.dot(syn1.T)
        l1_delta = l1_error * nonlin(l1, deriv=True)
        syn1 += l1.T.dot(l2_delta)
        syn0 += l0.T.dot(l1_delta)

        #print("output after training")
        #print(l2)
        #print(len(l2))

        '''for i in l2:
            if i > 0.7:
                print(type(i))'''


name = os.listdir("featureinputinnet/testfeatures")
name = sorted(name)
print(name)
count = 0
fp = open('featureinputinnet/final.txt', 'r', encoding='utf-8')
data = fp.read()
data = data.splitlines()
for k in range(0, 60000):
    count=0
    for i in name:
        final = []
        for j in data[count]:
            temp = []
            if j == str(0) or j == str(1):
                temp.append(int(j))
                final.append(temp)
        print(len(final))
        find(i, final,k)
        count += 1

np.save("syn0",syn0)
np.save("syn1",syn1)

#l2_error = y - l2
#print("Error:" + str(np.mean(np.abs(l2_error))))
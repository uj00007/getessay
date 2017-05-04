import numpy as np


def nonlin(x, deriv =False):
    if deriv == True:
        return (x*(1-x))
    return 1/(1+np.exp(-x))


syn0=np.load('syn0.npy')
syn1=np.load('syn1.npy')

print("this is testing now")
fp = open('featureinputinnet/testdoc.txt', 'r', encoding='utf-8')
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

x = np.array(flist)
print(type(x))
l0 = x
l1 = nonlin(np.dot(l0, syn0))  # np.dot is matrix multiplication
l2 = nonlin(np.dot(l1, syn1))
print("output after testing")
print(l2)
l=[]
l=l2.tolist()
print(l)
for i in range(0,len(l)):
    l[i].append(i+1)
print(l)
print(len(l2))
l=sorted(l,key=lambda x:(-x[0],x[1]))
print(l)
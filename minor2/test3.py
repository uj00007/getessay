import numpy as np
c=[]
a = np.array([[1],[0],[1]])
b = np.array([[1],[0],[1]])
c.append(a)
c.append(b)
a=np.concatenate((a,b))
#c=np.concatenate((c,a))
print(c[0])
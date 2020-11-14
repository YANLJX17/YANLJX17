import numpy as np
from scipy.sparse.linalg import svds
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

def get_matrix():
    matrix = np.zeros((64,360))
    k = 0
    with open("sys.in","r") as ma:
        for i in ma:
            i = i.split()
            for j in range(len(i)):
                matrix[k,j] = eval(i[j])
            k += 1
    return (matrix)
m = get_matrix()

#m = np.load("matrix_5d.npy").reshape(320,181*360)
#m = np.array([[1, 0, 0], [5, 0, 2], [0, -1, 0], [0, 0, 3.0]])

U,Sigma,VT = np.linalg.svd(m)
#U,Sigma,VT = svds(m,k = 2)

UT,V = U.transpose(),VT.transpose()
print(U.shape,V.shape)
for i in Sigma:
    print(i)
s_1 = 1 / Sigma
for i in s_1:
    print(i)
st = np.zeros((3,4))
for i in range(3):
    st[i,i] = s_1[i]
m_1 = V@st@UT
#m_1 = V@np.diag(s_1)@UT
print(m)
diag = m_1[:100,:320]@m[:320,:100]
#diag = m_1@m
print(diag)
fig,ax = plt.subplots(1,1,figsize = (64,64))
ax.imshow(diag,cmap='gray')
ax.set(title = "M@M^(-1)")
plt.savefig('SVD_TEST.png')

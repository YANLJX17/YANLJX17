import numpy as np
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

U,S,V,m = np.load("U.npy"),np.load("S.npy"),np.load("V.npy"),np.load("matrix_2d.npy")
print(U.shape,S.shape,V.shape,m.shape)
for i in range(320):
    S[i,i] = 1 / S[i,i]
m_1 = V @ S @ np.transpose(U)#matlab的svds函数返回的V为未转置的

test_points = np.zeros((181,360))
test_points[90,180] = 1
test_points = test_points.reshape((181*360,1))
test_points_p = m @ test_points
test_points_f = m_1 @ test_points_p

diag = m_1[:320,:]@m[:,:320]
x = np.zeros((360*181,1))
for i in range(360*181):
    x[i] = i
#print(diag)
fig,ax = plt.subplots(2,2,figsize = (64,64))
ax[0][0].imshow(diag)

ax[1][0].imshow(test_points_f.reshape((181,360)),cmap='gray')
plt.savefig('SVD_TEST.png')

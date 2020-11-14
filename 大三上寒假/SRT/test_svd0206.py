import numpy as np
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

m_1,sm,diag,imageline = np.load("m_1.npy"),np.load("sm.npy"),np.load("svd_diag.npy"),np.load("imageline.npy")


test_points = np.zeros((181,360))
test_points[90,180] = 1
test_points = test_points.reshape((181*360,1))
test_points_p = np.dot(sm,imageline)
test_points_f = np.dot(m_1,test_points_p)

for i in range(100):
    print(m_1[i,0])

fig,ax = plt.subplots(2,1,figsize = (64,64))
ax[0].imshow(diag)
ax[0].set(title = "M@M^(-1)")
ax[1].imshow(test_points_f.reshape((360,181)).transpose())
plt.savefig('SVD_TEST.png')
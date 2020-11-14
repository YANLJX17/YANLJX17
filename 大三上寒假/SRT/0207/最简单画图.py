import numpy as np

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

m_1 = np.load("test_mlem_90_180.npy")#无svd，直接局部mlem
m_2 = np.load("test_mlem_all_90_180.npy")#全局mlem
m_3 = np.load("test_svd_local_mlem_90_180.npy")#svd+local——mlem
m_4 = np.load("test_svd_90_180.npy")#svd

m_all = np.zeros((181,360))
m_all[81:102,169:190] = m_3.reshape((21,21)).transpose()
font1 = {'family': 'Times_New_Roman',
         'weight': 'normal',
         'size': 70,
         }
fig,ax = plt.subplots(3,1,figsize = (64,64))


ax[0].imshow(m_4.reshape((360,181)).transpose())
ax[1].imshow(m_2.reshape((360,181)).transpose())
ax[2].imshow(m_all)

ax[0].set_title("SVD",font1)
ax[1].set_title("MLEM",font1)
ax[2].set_title("SVD+local_MLEM",font1)


ax[0].set_ylabel(" θ",font1)
ax[0].set_xlabel(" φ",font1)
ax[1].set_ylabel(" θ",font1)
ax[1].set_xlabel(" φ",font1)
ax[2].set_ylabel(" θ",font1)
ax[2].set_xlabel(" φ",font1)
plt.savefig('test_mlem_90_180.png')

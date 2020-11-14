import scipy.io as io
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


xita,phi = 79,169
name = 'multiple_points_MCTS'
matr = io.loadmat(name+'.mat')
print(matr.keys())

#m_1 = matr["Image_Line"]
#s = matr['image']
s = matr['Recon_Result']


#保存为numpy数组文件（.npy文件）
np.save(name,s)
#np.save("imageline.npy",m_1)

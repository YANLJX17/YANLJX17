import scipy.io as io
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


xita,phi = 90,180
matr = io.loadmat('recon_mlem_all'+str(xita)+'_'+str(phi)+'.mat')
print(matr.keys())

#m_1 = matr["Image_Line"]
s = matr['recon_mlem']


#保存为numpy数组文件（.npy文件）
np.save('test_mlem_all_'+str(xita)+'_'+str(phi)+'.npy',s)
#np.save("imageline.npy",m_1)

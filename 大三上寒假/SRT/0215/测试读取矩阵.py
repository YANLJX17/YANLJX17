import numpy as np

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

m_1 = np.load("svd_mlem_recon.npy")

def bias(image,dot,mode = 0):
    '''
    输入image为重建后的图像（181*360）
    dot为原始图像的点源位置，为2*1数组
    输出为该点的定位偏差
    只适用于中度角度
    修改为局部模式，mode为1表示用图像中最亮的点作为中心点
    0215
    修改左右扩展的点数，为了使得
    '''
    xita,phi = 0,0
    counts_xita,counts_phi = 0,0
    x,y = dot[0],dot[1]
    if mode == 1:
        x,y = np.unravel_index(np.argmax(image),image.shape)
        #print("x,y",x,y)
    for i in range(181):
        for j in range(360):
            if abs(i - x) < 50:
                xita += i*image[i,j]
                counts_xita += image[i,j]
            if abs(j - y) < 50:
                phi += j*image[i,j]
                counts_phi += image[i,j]
    #all_counts = sum(sum(image))

    return xita/counts_xita - dot[0],phi/counts_phi - dot[1]
def fwhm(image,dot):
    '''
    输入image为重建后的图像（181*360），
    dot为原始图像的电源位置，为2*1数组
    输出为该点的分辨率
    只适用于中度角度
    0211
    '''
    x,y,inf = dot[0],dot[1],np.zeros((2,1))
    xita_fm,phi_fm = np.zeros((2,1)),np.zeros((2,1))
    for xita in range(90):
        if image[x-xita][y] < image[x][y]/2 and inf[0] == 0:
            xita_fm[0] = xita
            inf[0] = 1
        if image[x+xita][y] < image[x][y]/2 and inf[1] == 0:
            xita_fm[1] = xita
            inf[1] = 1
        if inf[0] == 1 and inf[1] == 1:
            inf = np.array([0,0])
            break
    
    for phi in range(180):
        if image[x,y - phi] < image[x,y]/2 and inf[0] == 0:
            phi_fm[0] = phi
            inf[0] = 1
        if image[x,y + phi] < image[x,y]/2 and inf[1] == 0:
            phi_fm[1] = phi
            inf[1] = 1
        if inf[0] == 1 and inf[1] == 1:
            break   
    return sum(sum(xita_fm)) - 2 ,sum(sum(phi_fm)) - 2#按照重建前图像的半高宽为0来标定

#print(bias(m_1,(90,179)),fwhm(m_1,(90,179)))
fig,ax = plt.subplots(2,2,figsize = (64,64))
ax[0][0].imshow(m_1[:,0,0].reshape((360,181)).transpose())
ax[0][0].set(title = "riginal")
ax[1][0].imshow(m_1[:,1,0].reshape((360,181)).transpose())
ax[1][0].set(title = "riginal")
ax[0][1].imshow(m_1[:,1,1].reshape((360,181)).transpose())
ax[0][1].set(title = "riginal")
ax[1][1].imshow(m_1[:,0,1].reshape((360,181)).transpose())
ax[1][1].set(title = "riginal")
plt.savefig('test_svd_mlem.png')
#print(m_1[:,0,0])
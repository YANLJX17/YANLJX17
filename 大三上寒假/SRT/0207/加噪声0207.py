import time 


import numpy as np
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

def std(m):
    n = np.zeros(len(m))
    maxm,minm = max(m),min(m)
    #print(maxm,minm)
    for i in range(len(m)):
        dt = maxm - minm
        n[i] = (m[i] - minm)/dt
        if n[i] > 1 or n[i] < 0:
            print("NO",m[i])
    return n

def poisson_noise(image):
    ''' 
        添加泊松噪声
        输入image为一维数组
    '''
    #image = np.array(image/255, dtype=float)
    image = std(image)
    l = 500#l调节计数大小
    print("all_counts",sum(l*image))
    for i in range(len(image)):
        image[i] = np.random.poisson(l*image[i])#注意不可以×倍数，倍数越高噪声越小
   
    out = image 
    #if out.min() < 0:
    #    low_clip = -1.
    #else:
    #    low_clip = 0.
    #out = np.clip(out, low_clip, 1.0)
    #out = np.uint8(out*255)
    #cv.imshow("gasuss", out)
    return out
    
def get_matrix_1(x = 63):
    '''
    参数x为保留的奇异值个数（由大到小排布）
    '''
    #使用svd(sm,"econ")的结果，再进行奇异值保留
    SE,UE,VE = np.load("SE.npy"),np.load("UE.npy"),np.load("VE.npy")

    for i in range(320):
        if i < x:
        #if SE[i,i] > 1e-8:
            SE[i,i] = 1/SE[i,i]
        else:
            SE[i,i] = 0
    me_1 = VE @ SE @ np.transpose(UE)
    
    return me_1

def bias(image,dot,mode = 0):
    '''
    输入image为重建后的图像（181*360）
    dot为原始图像的点源位置，为2*1数组
    输出为该点的定位偏差
    只适用于中度角度
    修改为局部模式，mode为1表示用图像中最亮的点作为中心点
    0215
    '''
    xita,phi = 0,0
    counts_xita,counts_phi = 0,0
    x,y = dot[0],dot[1]
    if mode == 1:
        x,y = np.unravel_index(np.argmax(image),image.shape)
        print("x,y",x,y)
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


if __name__ == "__main__":
    ##获取系统矩阵，伪逆
    m_1 = get_matrix_1(147)
    #m_1 = np.load("m_1.npy")
    sm = np.load("sm.npy")

    ##
    ##生成测试样例
    test_points = np.zeros((181,360))
    x,y = 90,180#均从1开始计数
    test_points = test_points.reshape((1,181*360)).transpose()
    test_points[(y-1)*181+x-1] = 1#由于matlab与python的reshape方式不同
    ##
    ##生成像空间数据，加噪声
    imageline = np.load("imageline.npy")
    test_points_p = np.dot(sm,test_points)
    test_points_pn = poisson_noise(test_points_p)
    ##
    ##生成重建图像(有噪声和无噪声)
    time_start=time.time()
    test_points_f,test_points_fn = np.dot(m_1,test_points_p).reshape((360,181)).transpose(),np.dot(m_1,test_points_pn).reshape((360,181)).transpose()
    time_end=time.time()
    print('totally cost',time_end-time_start,"s")
    ##
    ##测试重建图像的两个指标：偏离和分辨率
    print("xita,phi的加权偏移角度",bias(test_points_f,(x - 1,y - 1),mode = 0))#mode 为1表示用重建图像最亮点作为中心
    print("xita,phi的半高宽/°",fwhm(test_points_f,(x-1,y-1)))
    ##
    ##绘图
    fig,ax = plt.subplots(2,2,figsize = (64,64))
    ax[0][0].imshow(test_points.reshape((360,181)).transpose())
    ax[0][0].set(title = "riginal")
    ax[0][1].imshow(test_points_f)
    ax[0][1].set(title = "no_voice")
    ax[1][0].imshow(test_points_fn)
    ax[1][0].set(title = "voice")
    ax[1][1].imshow(m_1[:320,:]@sm[:,:320])
    ax[1][1].set(title = "m_1@m(320*320)")
    plt.savefig('SVD.png')

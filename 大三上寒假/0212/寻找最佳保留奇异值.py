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
    l = 10000#l调节计数大小
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
    result = []
    SE,UE,VE = np.load("SE.npy"),np.load("UE.npy"),np.load("VE.npy")
    for x in range(1,10):
        for i in range(x):
            if i < x:
                SE[i,i] = 1/SE[i,i]
            else:
                SE[i,i] = 0
        me_1 = VE @ SE @ np.transpose(UE)
        result.append(me_1)
    return me_1,result 

def bias(image,dot):
    '''
    输入image为重建后的图像（181*360），
    dot为原始图像的电源位置，为2*1数组
    输出为该点的定位偏差
    只适用于中度角度
    0211
    '''
    xita,phi = 0,0
    for i in range(181):
        for j in range(360):
            xita += i*image[i,j]
            phi += j*image[i,j]
    all_counts = sum(sum(image))

    return xita/all_counts - dot[0],phi/all_counts - dot[1]

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
    m_1,result = get_matrix_1()
    print(result)
    sm = np.load("sm.npy")
    ##
    ##生成测试样例
    x,y = 30,30#均从1开始计数
    test_points = np.zeros((181,360))
    test_points = test_points.reshape((1,181*360)).transpose()
    test_points[(y-1)*181+x-1] = 1#由于matlab与python的reshape方式不同
    ##
    ##生成像空间数据，加噪声
    imageline = np.load("imageline.npy")
    test_points_p = np.dot(sm,test_points)
    ##
    ##生成重建图像(有噪声和无噪声)
    test_points_f = np.dot(m_1,test_points_p).reshape((360,181)).transpose()
    ##
    ##测试重建图像的两个指标：偏离和分辨率
    print("xita,phi的半高宽/°",fwhm(test_points_f,(x-1,y-1)))

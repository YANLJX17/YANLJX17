import scipy.io as io
import numpy as np
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

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

def count_all_bias(s,i_x):
    global all_bias_result_svd_mlem_xita
    global all_bias_result_svd_mlem_phi
    info = 0
    for x in range(6):
        print(i_x,x)
        for y in range(301):
            if x == 0 and i_x == 1:
                x = 1
            tem_image = s[:,x,y].reshape((360,181)).transpose()
            #tem_image = np.zeros((181,360))#测试代码
            #tem_image[30 + 6*(i_x-1) + x - 1,30 + y-1] = 1
            bias_two = bias(tem_image,(30 + 6*(i_x-1) + x - 1,30 + y-1),mode = 0)
            #print(bias_two)
            all_bias_result_svd_mlem_xita[6*(i_x-1) + x - 1,y] = bias_two[0]#对于x还要考虑第几次输入问题，好确认下标
            all_bias_result_svd_mlem_phi[6*(i_x-1) + x - 1,y] = bias_two[1]
                
            if i_x == 21 and x == 1 and y == 300:
                info = 1
                break
        if info == 1:
            break

            


    #m_1 = matr["Image_Line"]

    #保存为numpy数组文件（.npy文件）
    #np.save('svd_mlem_recon.npy',s)
    #np.save("imageline.npy",m_1)
all_bias_result_svd_mlem_xita = np.zeros((121,301))
all_bias_result_svd_mlem_phi = np.zeros((121,301))
for i in range(1,22):
    #exec('conv(str(result_mlem{}))'.format(i))
    #name(i)
    
    matr = io.loadmat('result_svd_mlem'+ str(i) + ".mat")
    s = matr['result_svd_mlem'+ str(i)]
    count_all_bias(s,i)#修改了all_bias_result_svd_mlem_xita/phi
np.save("all_bias_result_svd_mlem_xita",all_bias_result_svd_mlem_xita)
np.save("all_bias_result_svd_mlem_phi",all_bias_result_svd_mlem_phi)

fig,ax = plt.subplots(2,2,figsize = (64,64))
ax[0][0].imshow(all_bias_result_svd_mlem_xita)
ax[0][0].set(title = "riginal")
ax[0][1].imshow(all_bias_result_svd_mlem_phi)
ax[0][1].set(title = "riginal")
plt.savefig('test_svd_mlem.png')
    #bias(s)
    
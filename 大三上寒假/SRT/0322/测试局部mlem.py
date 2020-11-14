import numpy as np
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt


def fwhm0322(image,dot):
    '''
    输入image为重建后的图像（181*360），
    dot为原始图像的点源位置，为2*1数组
    输出为该点的分辨率
    只适用于中度角度
    0211
    0322[版本更新]
    更改循环限为图片大小
    更改超出图片截断
    
    '''
    x,y,inf = dot[0],dot[1],np.zeros((2,1))
    xita_fm,phi_fm = np.zeros((2,1)),np.zeros((2,1))
    limit_xita,limit_phi = int(len(image)/2),int(len(image[0])/2)
    for xita in range(limit_xita):
        print("x-xita,len(image),x,y",x-xita,len(image),x,y)
        if x - xita < 0  and inf[0] == 0:
            xita_fm[0] = xita
            inf[0] = 1
        elif inf[0] == 0:
            if image[x-xita][y] < image[x][y]/2 : 
                xita_fm[0] = xita
                inf[0] = 1
        if x + xita >= len(image) and inf[1] == 0:
            xita_fm[1] = xita
            inf[1] = 1    
        elif inf[1] == 0:
            if image[x+xita][y] < image[x][y]/2 :
                xita_fm[1] = xita
                inf[1] = 1

        if inf[0] == 1 and inf[1] == 1:
            inf = np.array([0,0])
            break
    
    for phi in range(limit_phi):
        if y - phi < 0  and inf[0] == 0:
            phi_fm[0] = phi
            inf[0] = 1
        elif inf[0] == 0:
            if image[x,y - phi] < image[x,y]/2 :
                phi_fm[0] = phi
                inf[0] = 1


        if y + phi >= len(image[0])  and inf[1] == 0:
            phi_fm[1] = phi
            inf[1] = 1
        elif inf[1] == 0:
            if image[x,y + phi] < image[x,y]/2 : 
                phi_fm[1] = phi
                inf[1] = 1

        if inf[0] == 1 and inf[1] == 1:
            break   

    return sum(sum(xita_fm)) - 2 ,sum(sum(phi_fm)) - 2#按照重建前图像的半高宽为0来标定



def bias0322(image,dot,numpts = 50,mode = 0):
    '''
    输入image为重建后的图像（181*360）
    dot为原始图像的点源位置，为2*1数组
    输出为该点的定位偏差
    只适用于中度角度
    修改为局部模式，mode为1表示用图像中最亮的点作为中心点
    0215
    修改左右扩展的点数，为了使得
    0321
    注意dot要减一
    0322[版本更新]
    做加权的角度数可调
    将双循环部分的数字改为图像大小
    '''
    xita,phi = 0,0
    counts_xita,counts_phi = 0,0
    x,y = dot[0],dot[1]
    if mode == 1:
        x,y = np.unravel_index(np.argmax(image),image.shape)
        #print("x,y",x,y)
    for i in range(len(image)):
        for j in range(len(image[0])):
            if abs(i - x) < numpts:
                xita += i*image[i,j]
                counts_xita += image[i,j]
            if abs(j - y) < numpts:
                phi += j*image[i,j]
                counts_phi += image[i,j]
    #all_counts = sum(sum(image))
    #print(counts_xita,counts_phi)
    return xita/counts_xita - dot[0],phi/counts_phi - dot[1]

local_mlem = np.load("result_local_mlem.npy")
max_points = np.load("result_max_points.npy")
#定义储存量
result_local_mlem_all_space_bias = np.zeros((2,121,301))
result_local_mlem_all_space_fwhm = np.zeros((2,121,301))

#做偏移角的测量
for x in range(121):
    for y in range(301):
        #print(30+x-max_points[0,x,y]+10-1,30+y-max_points[1,x,y]+10-1)
        result_local_mlem_all_space_bias[:,x,y] = bias0322(local_mlem[:,x,y].reshape(21,21).transpose(),(30+x-max_points[0,x,y]+10,30+y-max_points[1,x,y]+10),10)
        ##半高宽老是有问题，貌似是输入的y有点误差？？？
        ##进行svd最大点验证是否偏差在10°以内工作
        if 30+x-max_points[0,x,y]+10 >= 21 or 30+x-max_points[0,x,y]+10 < 0 or 30+y-max_points[1,x,y]+10 >=21 or 30+y-max_points[1,x,y]+10 <0:
            print(x,y,30+x-max_points[0,x,y]+10,30+y-max_points[1,x,y]+10)
        #print("i,j",x,y)
        #result_local_mlem_all_space_fwhm[:,x,y] = fwhm0322(local_mlem[:,x,y].reshape(21,21).transpose(),(30+x-max_points[0,x,y]+10,30+y-max_points[1,x,y]+10))
        #if abs(sum(result_local_mlem_all_space_bias[:,x,y])) > 4:
            #print(x,y,result_local_mlem_all_space_bias[:,x,y])#,result_local_mlem_all_space_fwhm[:,x,y])
        

np.save('result_local_mlem_all_space_fwhm.npy',result_local_mlem_all_space_fwhm)
np.save('result_local_mlem_all_space_bias.npy',result_local_mlem_all_space_bias)
#绘图
fig,ax = plt.subplots(2,2,figsize = (100,100))

ax[0][0].imshow(result_local_mlem_all_space_bias,cmap = 'gray')

ax[1][1].imshow(result_local_mlem_all_space_fwhm,cmap = 'gray')

plt.savefig('test_mlem_.png')

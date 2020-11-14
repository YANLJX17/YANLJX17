import numpy as np

import numpy as np
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt


res = np.load("res_res_mode0_bias_f_all.npy")
bd_pit = 0
x,y,i_m = 0,0,0
im_res = [[0,0,0] for i in range (12)]
def turn_4d(res):
    res_4d = np.zeros((121,301,12,2))
    for i in range(len(res)):
        res_4d[int(res[i][0] - 30),int(res[i][1] - 30),int(res[i][2])][0] = res[i][3]
        res_4d[int(res[i][0] - 30),int(res[i][1] - 30),int(res[i][2])][1] = res[i][4]
    np.save("res_4d",res_4d)

for i in range(121*301*12):
    if abs(res[i][3]) >= 4 and abs(res[i][4]) >= 4:
        im_res[int(res[i][2])][2] += 1
    else:
        if abs(res[i][3]) >= 4:
            im_res[int(res[i][2])][0] += 1
        if abs(res[i][4]) >= 4:
            im_res[int(res[i][2])][1] += 1
            
        
    #if res[i][2] == 7:#结果表明为9是坏点最少的，大于5的只有60个点（phi）
    #    if abs(res[i][4]) >= 5:
     #       bd_pit = res[i][4]
     #       x,y = res[i][0],res[i][1]
      #      i_m += 1
print(im_res)

#def comm_bdpt(res):
#    for i in 
res_4d = np.load("res_4d.npy")#试验表明转化成功
im_res_2d =np.zeros((13,121,301))
for x in range(121):
    for y in range(301):
        for i in range(12):
            if abs(res_4d[x,y,i,1]) <= 4 :#and abs(res_4d[x,y,i,1]) <= 4:
                im_res_2d[12,x,y] = 1

            if abs(res_4d[x,y,i,0]) >= 4 and abs(res_4d[x,y,i,1]) >= 4:
                im_res_2d[i,x,y] = 1
            else:
                if abs(res_4d[x,y,i,0]) >= 4:
                    im_res_2d[i,x,y] += 1
                #if abs(res_4d[x,y,i,1]) >= 4:
                 #   im_res_2d[i,x,y] += 1

fig,ax = plt.subplots(4,4,figsize = (64,64))
for i in range(3):
    for j in range(4):
        ax[i][j].imshow(im_res_2d[j+4*i],cmap='gray')
ax[3][0].imshow(im_res_2d[12],cmap='gray')


plt.savefig('find_xita_bias4.png')

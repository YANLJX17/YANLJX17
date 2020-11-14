import numpy as np
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

img_bias = np.load('result_local_mlem_all_space_bias.npy')
tem_bias = np.zeros(img_bias.shape)

angle = 0

for x in range(121):
    for y in range(301):
        if abs(img_bias[0,x,y]) > angle:
            tem_bias[0,x,y] = 1
        #else:
        #    print(x,y,img_bias[0,x,y])
        if abs(img_bias[1,x,y]) > angle:
            tem_bias[1,x,y] = 1
        #else:
        #    print(x,y,img_bias[1,x,y])

local_mlem = np.load("result_local_mlem.npy")

#绘图
fig,ax = plt.subplots(4,2,figsize = (100,100))

ax[0][0].imshow(tem_bias[0,:,:],cmap = 'gray')
ax[0][0].set(title = 'xita')
ax[0][1].imshow(tem_bias[1,:,:],cmap = 'gray')
ax[0][1].set(title = 'phi')

ax[1][1].imshow(local_mlem[:,5,48].reshape(21,21).transpose())
ax[1][1].set(title = '5,48')
ax[1][0].imshow(local_mlem[:,5,162].reshape(21,21).transpose())
ax[1][0].set(title = '5,162')
ax[2][1].imshow(local_mlem[:,5,228].reshape(21,21).transpose())
ax[2][1].set(title = '5,228')
ax[2][0].imshow(local_mlem[:,117,48].reshape(21,21).transpose())
ax[2][0].set(title = '117,48')
ax[3][1].imshow(local_mlem[:,117,162].reshape(21,21).transpose())
ax[3][1].set(title = '117,162')
ax[3][0].imshow(local_mlem[:,117,228].reshape(21,21).transpose())
ax[3][0].set(title = '117,228')

plt.savefig('test_local_mlem_'+str(angle)+'.png')

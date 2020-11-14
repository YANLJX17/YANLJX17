import numpy as np
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

xita = np.load("all_bias_result_mlem_xita.npy")
phi = np.load("all_bias_result_mlem_phi.npy")
#ita_add4 = np.load("all_bias_result_svd_mlem_xita_add_4.npy")
#phi_add4 = np.load("all_bias_result_svd_mlem_phi_add_4.npy")
#xita_add29 = np.load("all_bias_result_svd_mlem_xita_add29.npy")
#phi_add29 = np.load("all_bias_result_svd_mlem_phi_add29.npy")
mlem_test = np.load("test_mlem_90_180.npy")

#for i in range(121):
#    print(xita_add29[i,0])

fig,ax = plt.subplots(2,2,figsize = (100,100))


#xita[4,:],phi[4,:] = xita_add4[4,:],phi_add4[4,:]
#xita[29,:],phi[29,:] = xita_add4[29,:],phi_add4[29,:]

#np.save("all_bias_result_svd_mlem_xita0320_add.npy",xita)
#np.save("all_bias_result_svd_mlem_phi0320_add.npy",phi)

tem_xita,tem_phi = np.zeros(xita.shape),np.zeros(xita.shape)
xita[4,:],phi[4,:] = tem_xita[4,:],tem_phi[4,:]
xita[29,:],phi[29,:] = tem_xita[29,:],tem_phi[29,:]

angle = 5

for x in range(121):
    for y in range(301):
        if abs(xita[x,y]) > angle:
            tem_xita[x,y] = 1
        if abs(phi[x,y]) > angle:
            tem_phi[x,y] = 1


ax[0][0].imshow(tem_xita,cmap = 'gray')
ax[0][0].set(title = "xita_"+str(angle))
ax[0][1].imshow(tem_phi,cmap = 'gray')
ax[0][1].set(title = "phi_"+str(angle))
ax[1][1].imshow(mlem_test.reshape((21,21)).transpose())

plt.savefig('test_mlem_'+str(angle)+'.png')
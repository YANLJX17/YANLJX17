import numpy as np

m_1,SE,UE,VE = np.load("m_1.npy"),np.load("SE.npy"),np.load("UE.npy"),np.load("VE.npy")
for i in range(320):
    if SE[i,i] > 1e-6:
        SE[i,i] = 1/SE[i,i]
    else:
        SE[i,i] = 0

me_1 = VE @ SE @ np.transpose(UE)

#for i in range(181*360):
#    for j in range(64*5):
#       if abs(me_1[i,j] - m_1[i,j]) > 1e-10:
#            print("no")
x = sum(sum(m_1))/(320*181*360)
print(x)
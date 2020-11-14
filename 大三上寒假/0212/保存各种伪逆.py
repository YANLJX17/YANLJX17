import numpy as np

def get_matrix(SE,UE,VE,y):
    '''
    参数x为保留的奇异值个数（由大到小排布）
    '''
    #使用svd(sm,"econ")的结果，再进行奇异值保留
    result = []
    S_1 = np.zeros((320,320))
    for x in range(y+1,y + 11):#是否应该改为y+1？是0215
        for i in range(320):#有bug，应该为for i in range(320):0215
            if i < x:
                S_1[i,i] = 1/SE[i,i]

        me_1 = VE @ S_1 @ np.transpose(UE)
        result.append(me_1)
        print(y,len(result))
    np.save("{}~{}_m_1.npy".format(y+1,y+10),result)

if __name__ == "__main__":
    SE,UE,VE = np.load("SE.npy"),np.load("UE.npy"),np.load("VE.npy")
    for i in range(150,151,10):
        get_matrix(SE,UE,VE,i)
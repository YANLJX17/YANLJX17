import numpy as np
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt


    
def get_matrix_1(x = 63):
    '''
    参数x为保留的奇异值个数（由大到小排布）
    '''
    #使用svd(sm,"econ")的结果，再进行奇异值保留
    SE,UE,VE = np.load("SE.npy"),np.load("UE.npy"),np.load("VE.npy")
    for i in range(320):
        if SE[i,i] > 1e-8:
            SE[i,i] = 1/SE[i,i]
        else:
            SE[i,i] = 0
    me_1 = VE @ SE @ np.transpose(UE)
    return me_1

if __name__ == "__main__":
    ##获取系统矩阵，伪逆
    m_1 = get_matrix_1()
    #m_1 = np.load("m_1.npy")
    sm = np.load("sm.npy")

    np.savetxt('a.txt',sm,fmt='%s',newline='\n')
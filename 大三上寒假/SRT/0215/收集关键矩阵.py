import numpy as np

def get_matrix(SE,UE,VE,y):
    '''
    参数y为保留的奇异值个数（由大到小排布）
    '''
    #使用svd(sm,"econ")的结果，再进行奇异值保留
    S_1 = np.zeros((320,320))
    for i in range(320):

        if i < y:
            S_1[i,i] = 1/SE[i,i]#不可反复使用SE这个变量名字，会造成SE被修改

    
    me_1 = VE @ S_1 @ np.transpose(UE)
    result = me_1
    print(y,len(result))
    return result

if __name__ == "__main__":
    SE,UE,VE = np.load("SE.npy"),np.load("UE.npy"),np.load("VE.npy")
    result = []
    for i in range(49,160,10):
        print(i)
        #get_matrix(SE,UE,VE,i)
        result.append(get_matrix(SE,UE,VE,i))
    np.save("important_m_1.npy",result)
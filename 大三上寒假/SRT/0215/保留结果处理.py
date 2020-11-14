import numpy as np

result = np.array(np.load("res_res.npy",allow_pickle=True))
sum_all_f = [0 for i in range(12)]
sum_all_fn = [0 for i in range(12)]
for i in range(0,13*31*12):
    #print(result[i])
    sum_all_f[int(result[i][2])] += result[i][5]
    sum_all_fn[int(result[i][2])] += result[i][6]
print(np.array(sum_all_f)/13/31,np.array(sum_all_fn)/13/31)
   
#保留结果应该为159个奇异值

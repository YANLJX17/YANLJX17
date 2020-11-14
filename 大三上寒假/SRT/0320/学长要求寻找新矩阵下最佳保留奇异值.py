import scipy.io as io
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


matr = io.loadmat('System_Matrix_MURAkeV.mat')
print(matr.keys())

#m_1 = matr["Image_Line"]
s = matr['System_Matrix']
s = s.reshape((320,181*360))
for x in range(len(s)):
    print(sum(abs(s[x])))
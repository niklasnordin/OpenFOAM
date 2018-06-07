import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

D = 0.04
U = 0.54
def calcZeroCrossing(x, y):
    t = []
    n = len(x)
    for i in range(0, n-1):
        y0 = y[i]
        y1 = y[i+1]
        if y0 < 0 and y1 > 0:
            t0 = x[i]
            t1 = x[i+1]
            tc = t0 - y0*(t1-t0)/(y1-y0)
            t.append(tc)
    return t

data = pd.read_csv("postProcessing/forces/0.000000e+00/coefficient_0.000000e+00.dat", skiprows=10, delimiter='\t', header=None)

t = data[0]
cm = data[1]
cd = data[2]
cl = data[3]
clf = data[4]
clr = data[5]
s = cl

times = calcZeroCrossing(t, s)
n = len(times)
dt = []
for i in range(0,n-1):
    dti = times[i+1]-times[i]
    dt.append(dti)

dt_calc = dt[30:]
dt_sum = sum(dt_calc)

cd_calc = cd[10000:]
cd_av = sum(cd_calc)/len(cd_calc)
av_dt = dt_sum/len(dt_calc)
St = D/(av_dt*U)
print("St = {}, Cd = {}".format(St, cd_av))
#fig, ax = plt.subplots()
#plt.plot(cd[10000:],'o')
#ax.grid()
#plt.show()

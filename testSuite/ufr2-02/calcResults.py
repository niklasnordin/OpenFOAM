import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("postProcessing/forces/0.000000e+00/coefficient_0.000000e+00.dat", skiprows=10, delimiter='\t', header=None)

t = data[0]
cm = data[1]
cd = data[2]
cl = data[3]
clf = data[4]
clr = data[5]

fig, ax = plt.subplots()
scat = ax.scatter(t,cl,s=1)
ax.grid()
ax.set_xlabel("Time [s]")
plt.show()

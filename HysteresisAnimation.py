
import csv
import qutip
import numpy as np
import scipy.optimize as opt
from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time



def plain(xy, a, b, d):
    x, y = xy
    return a*x + b*y +d #z = a*x + b*y +d

bloch= qutip.Bloch()
field = ["Ch", "Voltage", "Theta", "Eta", "DOP", "Power", "S1", "S2", "S3"]

data = np.empty((4, 4), dtype=object)
for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        data[i, j] = []

with open("csv/hysteresis_2025-03-27_11-38.csv", mode="r", newline="") as file:
    rdr = csv.DictReader(file)
    rdr.fieldnames = field
    for i in range(1,5):
        file.seek(0)
        s1 = np.array([])
        s2 = np.array([])
        s3 = np.array([])
        v = np.array([])
        for row in rdr:
            if(row["Ch"]==str(i)):
                data[i-1,0].append(float(row["S1"]))
                data[i-1,1].append(float(row["S2"]))
                data[i-1,2].append(float(row["S3"]))
                data[i-1,3].append(float(row["Voltage"]))



def update(j):
    bloch.clear()
    bloch.add_points([data[i,0][j], data[i,1][j], data[i,2][j]], colors='b', alpha=0.5)
    # per -5000 -> 5000; 5000 -> -5000 e 5000 -> -5000; -5000 -> 5000
    point_index=len(data[i,0])-1-j
    # per -5000 -> 5000; -5000 -> 5000 e 5000 -> -5000; 5000 -> -5000
    #point_index=dim+j

    bloch.add_points([data[i,0][point_index], data[i,1][point_index], data[i,2][point_index]], colors='r', alpha=0.5)
    bloch.make_sphere()
    text.set_text("Ch: "+str(i+1)+" Volt 1 : "+str(data[i,3][j])+" mV" + "  Volt 2 : "+str(data[i,3][point_index])+" mV")
    return ax, text

for i in range(4):
    fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
    bloch= qutip.Bloch()
    bloch.fig = fig  # Usa la figura di matplotlib per controllare il rendering
    text=fig.text(0.01, 0.01, " ", fontsize=12, color='black')
    dim = len(data[i,0])
    if dim%2 == 1:
        dim = dim - 1
    dim = int(dim/2)
    ani = animation.FuncAnimation(fig, update, frames=dim, interval=100, repeat=True)
    plt.show()

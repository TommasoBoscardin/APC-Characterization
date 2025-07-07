import csv
import qutip
import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt



def plain(xy, a, b, d):
    x, y = xy
    return a*x + b*y +d #z = a*x + b*y +d

bloch= qutip.Bloch()
fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
bloch.fig = fig
field = ["Ch", "Voltage", "Theta", "Eta", "DOP", "Power", "S1", "S2", "S3"]

data = np.empty((4, 4), dtype=object)
for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        data[i, j] = []

with open("csv/output_2025-03-27_10-17.csv", mode="r", newline="") as file:
    rdr = csv.DictReader(file)
    rdr.fieldnames = field
    for i in range(1,5):
        file.seek(0)
        for row in rdr:
            if(row["Ch"]==str(i)):
                data[i-1,0].append(float(row["S1"]))
                data[i-1,1].append(float(row["S2"]))
                data[i-1,2].append(float(row["S3"]))
                data[i-1,3].append(float(row["Voltage"]))

vect = np.empty((4,3))

for i in range(4):
    bloch.add_points([data[i,0], data[i,1], data[i,2]], alpha=0.5)
    parameters, covariance = opt.curve_fit(plain, (data[i,0],data[i,1]), data[i,2])
    a, b, _= parameters
    vect_t = [a, b, -1]
    vect[i] = vect_t/np.linalg.norm(vect_t)
#bloch.clear()
for i in range(4):
    bloch.add_vectors(vect[i])
    bloch.add_annotation(vect[i], i+1, fontsize=18, color='black')

bloch.add_arc(vect[0], vect[1])
bloch.add_arc(vect[1], vect[2])
bloch.add_arc(vect[2], vect[3])
bloch.add_arc(vect[3], vect[0])

ang12= np.rad2deg(np.arccos(np.dot(vect[0], vect[1])))
ang23= np.rad2deg(np.arccos(np.dot(vect[1], vect[2])))
ang34= np.rad2deg(np.arccos(np.dot(vect[2], vect[3])))
ang41= np.rad2deg(np.arccos(np.dot(vect[3], vect[0])))
print("ang12: ", ang12)
print("ang23: ", ang23)
print("ang34: ", ang34)
print("ang41: ", ang41)
fig.text(0.01, 0.1, r"$\angle v_1v_2$={:.2f}°".format(ang12), fontsize=20, color='black')
fig.text(0.01, 0.2, r"$\angle v_2v_3$={:.2f}°".format(ang23), fontsize=20, color='black')
fig.text(0.01, 0.3, r"$\angle v_3v_4$={:.2f}°".format(ang34), fontsize=20, color='black')
fig.text(0.01, 0.4, r"$\angle v_4v_1$={:.2f}°".format(ang41), fontsize=20, color='black')

bloch.show()

input("Press Enter to exit...")
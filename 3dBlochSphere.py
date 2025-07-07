import qutip
import csv
import numpy as np

bloch = qutip.Bloch()
field = ["Theta", "Eta", "DOP", "Power", "S1", "S2", "S3"]

data = np.empty(3, dtype=object)
for i in range(data.shape[0]):
    data[i] = []

with open("csv/scattered_2025-04-17_09-01.csv", mode="r", newline="") as file:
    rdr = csv.DictReader(file)
    rdr.fieldnames = field
    for row in rdr:
            if row["Theta"] == "Theta(Azimuth) [rad]":
                 continue
            data[0].append(float(row["S1"]))
            data[1].append(float(row["S2"]))
            data[2].append(float(row["S3"]))

with open("csv/scattered_2025-04-14_12-03.csv", mode="r", newline="") as file:
    rdr = csv.DictReader(file)
    rdr.fieldnames = field
    for row in rdr:
            if row["Theta"] == "Theta(Azimuth) [rad]":
                 continue
            data[0].append(float(row["S1"]))
            data[1].append(float(row["S2"]))
            data[2].append(float(row["S3"]))

bloch.add_points([data[0], data[1], data[2]])
bloch.show()

input("Press Enter to exit...")
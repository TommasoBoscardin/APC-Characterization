from polarimeter import ThorlabsPolarimeter as Polarimeter
from EPC400 import OZOpticsEPC400 as Controller
import time
import csv
from datetime import datetime
import os


plm = Polarimeter()
plm.connect()
plm.setWavelength(1.55e-6)
plm.setAvgMode(2)

cnt = Controller()
cnt.set_mode_ac()

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
filename = f"scattered_{timestamp}.csv"
folder = "csv"
os.makedirs(folder, exist_ok=True)  # Crea la cartella se non esiste
filepath = os.path.join(folder, filename)

T = 0.01 # Periodo di campionamento
t = 1800 # Tempo di acquisizione in secondi

with open(filepath, mode="w", newline="") as file:
    wrt = csv.writer(file)
    wrt.writerow(["Theta(Azimuth) [rad]", "Eta(Ellip) [rad]", "DOP [%]", "Power [W]", "S1 Normalized", "S2 Normalized", "S3 Normalized"])
    cnt.set_waveform_sine()
    cnt.set_frequency(1, 50)
    cnt.set_frequency(2, 60)
    cnt.set_frequency(3, 70)
    cnt.set_frequency(4, 80)
    pre_s1 = 0
    pre_s2 = 0
    pre_s3 = 0
    for i in range(0, int(t/T)):
        tmp = plm.getLastestDataAndStokes()
        if tmp[4]!=pre_s1 or tmp[5]!=pre_s2 or tmp[6]!=pre_s3:
            wrt.writerow([*tmp])
        pre_s1 = tmp[4]
        pre_s2 = tmp[5]
        pre_s3 = tmp[6]
        time.sleep(T)

del plm
del cnt
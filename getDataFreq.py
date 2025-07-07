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
filename = f"freq_{timestamp}.csv"
folder = "csv"
os.makedirs(folder, exist_ok=True)  # Crea la cartella se non esiste
filepath = os.path.join(folder, filename)

f = 5 # Frequenza in Hz
t = 180 # Tempo di acquisizione in secondi
""" s = 10 # Numero di campioni per secondo
T = 1/(s*f) # Periodo di campionamento """

with open(filepath, mode="w", newline="") as file:
    wrt = csv.writer(file)
    wrt.writerow(["DAC_Number", "Time [s]", "Theta(Azimuth) [rad]", "Eta(Ellip) [rad]", "DOP [%]", "Power [W]", "S1 Normalized", "S2 Normalized", "S3 Normalized"])
    cnt.set_waveform_triangle()
    for ch in range(1,5):
        cnt.set_frequency(1, 0)
        cnt.set_frequency(2, 0)
        cnt.set_frequency(3, 0)
        cnt.set_frequency(4, 0)
        ti = time.time()
        cnt.set_frequency(ch, f)
        res = t
        tp = ti
        pre_s1 = 0
        pre_s2 = 0
        pre_s3 = 0
        while res > 0:
            tf = time.time()
            tmp = plm.getLastestDataAndStokes()
            if tmp[4]!=pre_s1 or tmp[5]!=pre_s2 or tmp[6]!=pre_s3:
                wrt.writerow([ch, tf-ti, *tmp])
            pre_s1 = tmp[4]
            pre_s2 = tmp[5]
            pre_s3 = tmp[6]
            res = res - (tf - tp)
            tp = tf
            print(f"Channel: {ch}, Time Remaining: {res:.2f} seconds")
            #time.sleep(0.05)
        time.sleep(1)
        

del plm
del cnt
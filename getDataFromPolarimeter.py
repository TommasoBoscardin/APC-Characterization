from polarimeter import ThorlabsPolarimeter as Polarimeter
from EPC400 import OZOpticsEPC400 as Controller
import time
import csv
from datetime import datetime
import os

plm = Polarimeter()         # Inizializza il polarimetro
plm.connect()
plm.setWavelength(1.55e-6)  # Imposta la lunghezza d'onda a 1550 nm
plm.setAvgMode(9)           # Imposta la Operation Mode a 9

cnt = Controller()          # Inizializza il controller
cnt.set_mode_dc()           # Imposta il controller in modalità DC  

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
filename = f"output_{timestamp}.csv"
folder = "csv"
os.makedirs(folder, exist_ok=True)  # Crea la cartella se non esiste
filepath = os.path.join(folder, filename)
with open(filepath, mode="w", newline="") as file: # Crea un file CSV con il timestamp
    wrt = csv.writer(file)
    wrt.writerow(["DAC_Number", "Voltage [mV]", "Theta(Azimuth) [rad]", "Eta(Ellip) [rad]", "DOP [%]", "Power [W]", "S1 Normalized", "S2 Normalized", "S3 Normalized"])
    for ch in range(1,5):                       # Loop per i canali 1-4 
        for volt in range(-5000, 5001, 100):    # Loop per i valori di tensione da -5000 a 5000 mV
            cnt.set_voltage(ch, volt)           # Imposta la tensione del canale corrente
            time.sleep(1)                       # Attende 1 secondo 
            wrt.writerow([ch, volt, *plm.getLastestData(), *plm.getStokesVector()]) # Scrive i dati nel file CSV
        time.sleep(1)

del plm
del cnt

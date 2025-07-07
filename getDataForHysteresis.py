from polarimeter import ThorlabsPolarimeter as Polarimeter
from EPC400 import OZOpticsEPC400 as Controller
#from EPCDriver import OZOpticsEPC as Epc
import time
import csv
from datetime import datetime
import os


plm = Polarimeter()
plm.connect()
plm.setWavelength(1.55e-6)
plm.setAvgMode(9)

cnt = Controller()
cnt.set_mode_dc()

#epc = Epc()
#epc.autoconnect()
#epc.setDC()


timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
filename = f"hysteresis_{timestamp}.csv"
folder = "csv"
os.makedirs(folder, exist_ok=True)  # Crea la cartella se non esiste
filepath = os.path.join(folder, filename)
with open(filepath, mode="w", newline="") as file:
    wrt = csv.writer(file)
    wrt.writerow(["DAC_Number", "Voltage [mV]", "Theta(Azimuth) [rad]", "Eta(Ellip) [rad]", "DOP [%]", "Power [W]", "S1 Normalized", "S2 Normalized", "S3 Normalized"])
    for ch in range(1,5):
        """ for volt in range(-5000, 5001, 100):
            cnt.set_voltage(ch, volt)
            #cnt.set_mode_dc()
            time.sleep(1)
            wrt.writerow([ch, volt, *plm.getLastestData(), *plm.getStokesVector()])
            print(f"Ch: {ch} Volt: {volt} mV")
        for volt in range(5000, -5001, -100):
            cnt.set_voltage(ch, volt)
            #cnt.set_mode_dc()
            time.sleep(1)
            wrt.writerow([ch, volt, *plm.getLastestData(), *plm.getStokesVector()])
            print(f"Ch: {ch} Volt: {volt} mV")
        for volt in range(-5000, 5001, 100):
            cnt.set_voltage(ch, volt)
            #cnt.set_mode_dc()
            time.sleep(1)
            wrt.writerow([ch, volt, *plm.getLastestData(), *plm.getStokesVector()])
            print(f"Ch: {ch} Volt: {volt} mV")
        for volt in range(5000, -5001, -100):
            cnt.set_voltage(ch, volt)
            #cnt.set_mode_dc()
            time.sleep(1)
            wrt.writerow([ch, volt, *plm.getLastestData(), *plm.getStokesVector()])
            print(f"Ch: {ch} Volt: {volt} mV")
        time.sleep(1) """
        volt = -5000
        cnt.set_voltage(ch, volt)
        time.sleep(1)
        wrt.writerow([ch, volt, *plm.getLastestData(), *plm.getStokesVector()])
        volt = 5000
        cnt.set_voltage(ch, volt)
        time.sleep(1)
        wrt.writerow([ch, volt, *plm.getLastestData(), *plm.getStokesVector()])
        volt = -5000
        cnt.set_voltage(ch, volt)
        time.sleep(1)
        wrt.writerow([ch, volt, *plm.getLastestData(), *plm.getStokesVector()])
        volt = 5000
        cnt.set_voltage(ch, volt)
        time.sleep(1)
        wrt.writerow([ch, volt, *plm.getLastestData(), *plm.getStokesVector()])

del plm
del cnt
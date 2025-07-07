# -*- coding: utf-8 -*-
"""
Created on Mon May  3 09:43:15 2021
            else:

@author: Elisa Bazzani
"""

import pyvisa as visa
import numpy as np
import cmath
import csv
from PyQt5.QtCore import QDateTime
import os
import qutip



class ThorlabsPolarimeter :
    
    def __init__(self):
        self.res = 0 # meaningless init
    
         
    def connect(self):
        rm = visa.ResourceManager()
        resources = rm.list_resources()
        id_string = "THORLABS,PAX"
        
        if len(resources) == 0:
            print("No VISA resources found")
            return False
        else:
            for res in resources:
                inst = rm.open_resource(res)
                string = inst.query("*IDN?")
                if id_string in string:
                    break    
            self.res = inst

            self.res.write("INP:ROT:STAT ON") #Set ON the motor
                
            return True
        

    
    def getWavelength(self):
        return self.res.query("SENS:CORR:WAV?")
    
    def setWavelength(self, value):
        self.res.write("*CLS")
        self.res.write("SENS:CORR:WAV " + str(value))
        err = self.res.query("SYST:ERR:NEXT?")
        if err[0] != "0":
           ThorlabsPolarimeter.errorHandling(err)
            
    
    """
    Set the averaging mode
    Parameter: integer number in range [0,9] 
    0 = IDLE
    1 = H512 (half waveplate rotation with 512 point FFT)
    2 = H1024
    3 = H2048
    4 = F512
    5 = F1024 (one full waveplate rotation with 1024 point FFT)
    6 = F2048
    7 = D512
    8 = D1024
    9 = D2048 (two waveplate rotations with 2048 point FFT)
    
    """
    def setAvgMode(self, mode):
        self.res.write("*CLS")
        self.res.write("SENS:CALC:MOD " + str(mode))
        err = self.res.query("SYST:ERR:NEXT?")
        if err[0] != "0":
            ThorlabsPolarimeter.errorHandling(err)
            
    def getAvgMode(self):
        return self.res.query("SENS:CALC:MOD?")
    
    def getRotorVel(self):
        self.res.write("INP:ROT:VEL 50")
        return self.res.query("INP:ROT:VEL?")
         
    """
    Get last measurement set of data
    return: numpy array with positions
    1 = Stokes Azimuthal angle
    2 = Stokes Ellipticity
    3 = Degree Of Polarization
    4 = Total Power
    
    """      
    def getLastestData(self):
        self.res.write("*CLS")
        data = self.res.query("SENS:DATA:LAT?").split(",")
        
        #print(self.res.query("SENS:DATA:LAT?"))
        #print(data)
        
        theta = data[9] #azimuth radianti
        eta = data[10] #ellip radinati
        DOP = data[11] 
        Ptotal = data[12] #Watt
        
        err = self.res.query("SYST:ERR:NEXT?")
        
        if err[0] != "0":
            ThorlabsPolarimeter.errorHandling(err)
            return
        
        else:     
    
            return np.array([theta,eta,DOP,Ptotal], dtype = "double")
        
    def getStokesVector(self):
        meas = self.getLastestData()
        theta = meas[0]
        eta = meas[1]
        s1=np.cos(2*theta)*np.cos(2*eta) #H
        s2=np.sin(2*theta)*np.cos(2*eta) #D
        s3=np.sin(2*eta)                 #R
        
        return np.array([s1, s2, s3])
        
    def getLastestDataAndStokes(self):
        self.res.write("*CLS")
        data = self.res.query("SENS:DATA:LAT?").split(",")
        
        #print(self.res.query("SENS:DATA:LAT?"))
        #print(data)
        
        theta = data[9] #azimuth radianti
        eta = data[10] #ellip radinati
        DOP = data[11] 
        Ptotal = data[12] #Watt
        
        err = self.res.query("SYST:ERR:NEXT?")
        
        if err[0] != "0":
            ThorlabsPolarimeter.errorHandling(err)
            return
        
        else:     
    
            return np.array([theta,eta,DOP,Ptotal,np.cos(2*float(theta))*np.cos(2*float(eta)), np.sin(2*float(theta))*np.cos(2*float(eta)), np.sin(2*float(eta))], dtype = "double")
        
    def getJonesVect(self):
        meas = self.getLastestData()
        thetaStokes = meas[0]
        etaStokes = meas[1]
        
        theta = np.arccos(np.cos(2*etaStokes)*np.cos(2*thetaStokes))

        if theta != 0:
            
            cosPhi = np.cos(2*etaStokes)*np.sin(2*thetaStokes)/np.sin(theta)
            sinPhi = np.sin(2*etaStokes)/np.sin(theta)
            if np.sign(cosPhi) == 0 or np.sign(sinPhi) == 0 :
                if np.sign(cosPhi) == 0:
                    phi = np.arcsin(sinPhi)
                else :
                    phi = np.arccos(cosPhi)
                        
            elif np.sign(cosPhi) > 0 and np.sign(sinPhi) > 0 :
                phi = np.arcsin(sinPhi) #because arcsin belongs to -pi/2 - pi/2
                    
            elif np.sign(cosPhi) < 0 and np.sign(sinPhi) > 0 :
                phi = np.arccos(cosPhi) #because arccos belongs to 0 - pi
                    
            elif np.sign(cosPhi) < 0 and np.sign(sinPhi) < 0 :
                phi = np.pi - np.arcsin(sinPhi)
                    
            else : # cos>0 and sin<0
                phi = np.arcsin(sinPhi)
            
            jones = np.array([np.cos(theta/2), cmath.exp(phi*1j)*np.sin(theta/2)])
            
        else:
            jones = np.array([np.cos(theta/2), 0]) #If theta = 0, nevertheless phi (global phase term), we have H
 
        return jones
    
    def getAngularCoordOnBloch(self):
        
        
        meas = self.getLastestData()
        thetaStokes = meas[0]
        etaStokes = meas[1]
        
        theta = np.arccos(np.cos(2*etaStokes)*np.cos(2*thetaStokes))

        if theta != 0:
            
            cosPhi = np.cos(2*etaStokes)*np.sin(2*thetaStokes)/np.sin(theta)
            sinPhi = np.sin(2*etaStokes)/np.sin(theta)
            if np.sign(cosPhi) == 0 or np.sign(sinPhi) == 0 :
                if np.sign(cosPhi) == 0:
                    phi = np.arcsin(sinPhi)
                else :
                    phi = np.arccos(cosPhi)
                        
            elif np.sign(cosPhi) > 0 and np.sign(sinPhi) > 0 :
                phi = np.arcsin(sinPhi) #because arcsin belongs to -pi/2 - pi/2
                    
            elif np.sign(cosPhi) < 0 and np.sign(sinPhi) > 0 :
                phi = np.arccos(cosPhi) #because arccos belongs to 0 - pi
                    
            elif np.sign(cosPhi) < 0 and np.sign(sinPhi) < 0 :
                phi = np.pi - np.arcsin(sinPhi)
                    
            else : # cos>0 and sin<0
                phi = np.arcsin(sinPhi)
                
        else:
            phi = 0
            print ("theta = 0 so phi is arbitrary, horizontal state")
         
            
        return np.array([theta, phi])

    
    def getStateOnBlochSphere(self):
        
        meas = self.getAngularCoordOnBloch()
        theta = meas[0]
        phi = meas[1]
        
        return [np.sin(theta)*np.cos(phi), np.sin(theta)*np.sin(phi), np.cos(theta)]
    
    
    def writeToLog(self, filePath):
        angles = self.getAngularCoordOnBloch()
        theta = angles[0]
        phi = angles[1]
        DOP = self.getLastestData()[2]
        Ptot = self.getLastestData()[3]
        
        
        time=QDateTime.currentDateTime()
        timeDisplay=time.toString('yyyy:MM:dd hh:mm:ss dddd')
        
        
        file = '/polarimeterLog.csv'
        
        fields = ['Time', 'theta [deg]', 'phi [deg]', 'DOP', 'Power [W]']
        
        if os.path.exists(filePath + file):
            with open(filePath + file,'a', encoding='UTF8', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvfile.write("")
                csvwriter.writerow([timeDisplay, theta, phi, DOP, Ptot])
     
        else :
            with open(filePath + file, 'a', encoding='UTF8', newline='') as csvfile: 
                csvwriter = csv.writer(csvfile) 
                csvwriter.writerow(fields) 
                csvwriter.writerow([timeDisplay, theta, phi, DOP, Ptot])
    

        
        
    
    @staticmethod    
    def errorHandling(err):
        print("Error = " + err)
        
        


"""
def main():
    polarObj = ThorlabsPolarimeter()
    polarObj.connect()
    polarObj.setWavelength(1.55e-6)
    polarObj.setAvgMode(9)
    print("JonesVector: ",polarObj.getJonesVect())
    print("AngularCoordOnBloch: ",polarObj.getAngularCoordOnBloch())
    print("StateOnBlochSphere: ",polarObj.getStateOnBlochSphere())
    print("Data: ",polarObj.getLastestData())

    print("Stokes Vector: ", polarObj.getStokesVector())

    bloch= qutip.Bloch()
    bloch.add_points(polarObj.getStokesVector())
    bloch.show()
    input(" ")
    

if __name__ == "__main__":
    main()
"""

 



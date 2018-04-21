# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 23:20:16 2017

@author: arthu
"""

#from IPython import get_ipython
#get_ipython().magic('reset -sf') 

import sys
import numpy as np
import cantera as ct
import matplotlib.pyplot as plt
import csv
from scipy.interpolate import interp1d 
import math

#fuel=input('Which Fuel? \t\n[1]\tTPRF EEE'+'\n[2]\tIsoOctane'+'\n[3]\tEEE'+'\n[4]\tTPRF-Iso\n')
#if fuel=='1':
#    #"""For TPRF"""
#    gas1 = ct.Solution('TRF_EtOH_PAH.cti')
#    RON=96.3; MON=88.8; S=RON-MON; Phi=1.0
#    x_tol=S/14.07 #toluene mole fraction per Eq ??
#    PRF=(RON-118.09*x_tol+1.777)/(1.0023-1.0355*x_tol) # PRF of iC8-nC7 mixture per Eq ?
#    ni_nn=(0.692*100.2)/(0.684*114.2)*(PRF/100)/(1-PRF/100) #volume fraction to mole fraction conversion
#    # rho_iso=0.692; rho_nhep=).684; MW_iso=114.2; MW_nhep=100.2
#    x_nhep=(1-x_tol)/(1+ni_nn)
#    x_iso=1-x_tol-x_nhep
#    x_init=np.zeros(gas1.X.shape)
#    x_init[gas1.species_index('c7h8')]=x_tol
#    x_init[gas1.species_index('ic8h18')]=x_iso
#    x_init[gas1.species_index('nc7h16')]=x_nhep
#
#elif fuel=='2':
#      #"""For Iso-Octane"""  
#      gas1 = ct.Solution('ic8_ver3_mech.cti')
#      Phi=1.0
#      x_nhep=0
#      x_iso=1
#      x_tol=0
#      x_init=np.zeros(gas1.X.shape)
#      x_init[gas1.species_index('ic8h18')]=x_iso
#
#elif fuel=='3':
#    Phi=1.0
#    gas1 = ct.Solution('TRF_EtOH_PAH.cti')
#    x_tol=0.3
#    x_nhep=0.1377
#    x_iso=0.5673              
#    x_init=np.zeros(gas1.X.shape)
#    x_init[gas1.species_index('c7h8')]=x_tol
#    x_init[gas1.species_index('ic8h18')]=x_iso
#    x_init[gas1.species_index('nc7h16')]=x_nhep
#
#elif fuel=='4':
#    #"""For TPRF"""
#    gas1 = ct.Solution('TRF_EtOH_PAH.cti')
#    RON=100; MON=100; S=RON-MON; Phi=1.0
#    x_tol=S/14.07 #toluene mole fraction per Eq ??
#    PRF=(RON-118.09*x_tol+1.777)/(1.0023-1.0355*x_tol) # PRF of iC8-nC7 mixture per Eq ?
#    ni_nn=(0.692*100.2)/(0.684*114.2)*(PRF/100)/(1-PRF/100) #volume fraction to mole fraction conversion
#    # rho_iso=0.692; rho_nhep=).684; MW_iso=114.2; MW_nhep=100.2
#    x_nhep=(1-x_tol)/(1+ni_nn)
#    x_iso=1-x_tol-x_nhep
#    x_init=np.zeros(gas1.X.shape)
#    x_init[gas1.species_index('c7h8')]=x_tol
#    x_init[gas1.species_index('ic8h18')]=x_iso
#    x_init[gas1.species_index('nc7h16')]=x_nhep
"""=================================================="""
#gas1 = ct.Solution('ic8_ver3_mech.cti')
#gas1 = ct.Solution('LLNL_gasoline_20170621_nox_galway.cti')
gas1 = ct.Solution('RenKokjohn.cti')
x_init=np.zeros(gas1.X.shape)
c4=0#ws['E12'].value #0.01      #n-butane
c5=0#ws['E13'].value #0.0      #iso-pentane
c5_2=0#ws['E14'].value #0.04   #n-pentane
ic8=1#ws['E15'].value #0.93    #Iso-octane
c6=0#ws['E16'].value #0.0      #added for 1-hexene
nc7=0#ws['E17'].value #0.0    #n-heptane
c7_2=0#ws['E18'].value #0.0    #tolune
tmb=0#ws['E19'].value #0.02     #1,2,4 Trimethyl benzene 
eth=0#ws['E20'].value #0       #Ethanol
Phi=1   

#x_init[gas1.species_index('nC7h16')]=nc7
x_init[gas1.species_index('ic8h18')]=ic8
#x_init[gas1.species_index('IC8')]=ic8
x_init[gas1.species_index('C2H5OH')]=eth
#x_init[gas1.species_index('c7h8')]=c7_2
#x_init[gas1.species_index('C6H5CH3')]=c7_2
print(ic8)
print(nc7)
print(tmb)
print(eth)
## Determine global composition

nC=(4*c4)+(5*c5)+(5*c5_2)+(6*c6)+(7*nc7)+(8*ic8)+(9*tmb)+(2*eth)+(7*c7_2)
nH=(10*c4)+(12*c5)+(12*c5_2)+(12*c6)+(16*nc7)+(18*ic8)+(12*tmb)+(6*eth)+(8*c7_2)
nO=1*eth
print(nC)
print(nH)
print(nO)

x_init[gas1.species_index('O2')]=(nC+nH/4-nO/2)/Phi
x_init[gas1.species_index('N2')]=3.76*(nC+nH/4-nO/2)/Phi
#    gas.TPX= 300, 1e5, x_init         

#nC=8*x_iso+7*(x_nhep+x_tol)
#nH=18*x_iso+16*x_nhep+8*x_tol
#x_init[gas1.species_index('o2')]=(nC+nH/4)/Phi
#x_init[gas1.species_index('n2')]=3.76*(nC+nH/4)/Phi      

# handle the arguemnts
if len(sys.argv) != 2:
    print ("Error: Must have a jobid arguement\nUsage: python Ignition_Delay_Temp_ALG.py jobid")
    exit(1)

jobid = (int)(sys.argv[1])

ig_press_cont=np.linspace(1e5,50e5,30)
#ig_press_cont=np.linspace(1e5,50e5,1000)
low_res=np.array([400,500])
high_res=np.array(np.linspace(600,1000,30))
#high_res=np.array(np.linspace(600,1000,500))
ig_temp_cont=np.concatenate((low_res,high_res),axis=0)       
IG_Temp,IG_Press=np.meshgrid(ig_temp_cont,ig_press_cont,indexing='ij')  #Meshgrid for plotting        
#tau_arr=np.zeros((np.size(ig_temp_cont),np.size(ig_press_cont)))
#Final_temp=np.zeros((np.size(ig_temp_cont),np.size(ig_press_cont)))

# divide the double for loop into 32*30 parallel jobs
temp_idx, pres_idx = jobid/len(ig_temp_cont), jobid%len(ig_temp_cont)
curr_temp, curr_pres = ig_temp_count[temp_idx], ig_press_cont[pres_idx]

#for n in range (0,np.size(ig_temp_cont)):#32
    #for o in range (0,np.size(ig_press_cont)):#30

print("job_id:{} temperature:{} pressure:{}".format(jobid, curr_temp. curr_pres))
gas1.TPX=curr_temp,curr_pres,x_init
r1=ct.IdealGasReactor(gas1)     #Ignition Delay reactor    
sim2= ct.ReactorNet([r1])    
time=0      #Initialize Time
Temp_cur=0#ig_temp_cont[n]
Press_cv=[]
Temp_cv=[]
timeapp=[]
while (Temp_cur < curr_temp+50 and time < 20e-3):
    time += 1.e-6
    sim2.advance(time)
    time_cur=time #milliseconds
    Press=r1.thermo.P
    Temp=r1.T
    Temp_cur=Temp
#            times.append(time_cur)
    Press_cv.append(Press)
    Temp_cv.append(Temp)
    timeapp.append(time)

# save the output for each job
# outputs includes: Final_temp, tau_arr
print(Temp)
print(time_cur)

'''
conlevels=np.arange(1e-3,10e-3,1e-3)
plt.figure
plt.rcParams.update({'font.size': 30})
CS=plt.contour(IG_Temp,IG_Press/1e5,tau_arr,levels=conlevels)
plt.clabel(CS, inline=1, fontsize=20)
cb=plt.colorbar()
cb.ax.tick_params(labelsize=20)
'''
#np.save('LLNL_iso_mech_IGPress',IG_Press)
#np.save('LLNL_iso_mech_IGTemp',IG_Temp)
#np.save('LLNL_iso_mech_Tau',tau_arr)
#np.save('LLNL_iso_mech_FinalTemp',Final_temp)
#np.savefig('IgdelayLLNL')

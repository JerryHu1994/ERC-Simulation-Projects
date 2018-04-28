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
#import matplotlib.pyplot as plt
import csv
#from scipy.interpolate import interp1d 
import math


"""=================================================="""
#gas = ct.Solution('ic8_ver3_mech.cti')
gas = ct.Solution('LLNL_gasoline_20170621_nox_galway.cti')
#gas = ct.Solution('RenKokjohn.cti')
x_init=np.zeros(gas.X.shape)
c4=.01#ws['E12'].value #0.01      #n-butane
c5=0#ws['E13'].value #0.0      #iso-pentane
c5_2=.04#ws['E14'].value #0.04   #n-pentane
ic8=.93#ws['E15'].value #0.93    #Iso-octane
c6=0#ws['E16'].value #0.0      #added for 1-hexene
nc7=0#ws['E17'].value #0.0    #n-heptane
c7_2=0#ws['E18'].value #0.0    #tolune
tmb=.02#ws['E19'].value #0.02     #1,2,4 Trimethyl benzene 
eth=0#ws['E20'].value #0       #Ethanol
Phi=1   

"""Renkokjohn Composition"""
##x_init[gas.species_index('nC7h16')]=nc7
#x_init[gas.species_index('ic8h18')]=ic8
##x_init[gas.species_index('IC8')]=ic8
#x_init[gas.species_index('C2H5OH')]=eth
##x_init[gas.species_index('c7h8')]=c7_2
##x_init[gas.species_index('C6H5CH3')]=c7_2
#print(ic8)
#print(nc7)
#print(tmb)
#print(eth)

"""LLNL Composition"""
x_init[gas.species_index('C4H10')]=c4
x_init[gas.species_index('IC5H12')]=c5
x_init[gas.species_index('NC5H12')]=c5_2
x_init[gas.species_index('C6H12-1')]=c6
x_init[gas.species_index('NC7H16')]=nc7
x_init[gas.species_index('C6H5CH3')]=c7_2
x_init[gas.species_index('IC8')]=ic8
x_init[gas.species_index('T124MBZ')]=tmb
x_init[gas.species_index('C2H5OH')]=eth
## Determine global composition


carbon=np.zeros(gas.X.size); 
hydrogen=np.zeros(gas.X.size);
oxygen=np.zeros(gas.X.size)
for i in range(gas.n_species):
    carbon[i]=gas.n_atoms(i,'C')
    hydrogen[i]=gas.n_atoms(i,'H')
    oxygen[i]=gas.n_atoms(i,'O')
    nC=np.dot(x_init,carbon)
    nH=np.dot(x_init,hydrogen)
    nO=np.dot(x_init,oxygen)

#nC=(4*c4)+(5*c5)+(5*c5_2)+(6*c6)+(7*nc7)+(8*ic8)+(9*tmb)+(2*eth)+(7*c7_2)
#nH=(10*c4)+(12*c5)+(12*c5_2)+(12*c6)+(16*nc7)+(18*ic8)+(12*tmb)+(6*eth)+(8*c7_2)
#nO=1*eth
#print(nC)
#print(nH)
#print(nO)

x_init[gas.species_index('O2')]=(nC+nH/4-nO/2)/Phi
x_init[gas.species_index('N2')]=3.76*(nC+nH/4-nO/2)/Phi
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
low_res=np.array([400,500])
high_res=np.array(np.linspace(600,1000,30))
ig_temp_cont=np.concatenate((low_res,high_res),axis=0)       
IG_Temp,IG_Press=np.meshgrid(ig_temp_cont,ig_press_cont,indexing='ij')  #Meshgrid for plotting        
#tau_arr=np.zeros((np.size(ig_temp_cont),np.size(ig_press_cont)))
#Final_temp=np.zeros((np.size(ig_temp_cont),np.size(ig_press_cont)))


# divide the double for loop into 32*30 parallel jobs
pres_idx = jobid
curr_pres = ig_press_cont[pres_idx]

#for n in range (0,np.size(ig_temp_cont)):# 32 jobs
    #print(n)
    #for o in range (0,np.size(ig_press_cont)):# 30 jobs
tau_result = np.zeros((32))
temp_result = np.zeros((32))
pres_result = np.zeros((32))
for idx in range(len(ig_temp_cont)):
    curr_temp = ig_temp_cont[idx]
    print("job_id:{} pressure:{} temperature: {}".format(jobid, curr_pres, curr_temp))        
    gas.TPX=curr_temp,curr_pres,x_init    
    r1=ct.IdealGasReactor(gas)     #Ignition Delay reactor    
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
    tau_result[idx] = time_cur
    temp_result[idx] = Temp
    pres_result[idx] = Press
    #Final_temp[n,o]=Temp     
    #tau_arr[n,o]=(time_cur)
     
# save the output for each job
# outputs includes: Final_temp, tau_arr

'''
conlevels=np.arange(1e-3,10e-3,1e-3)
plt.figure
plt.rcParams.update({'font.size': 30})
CS=plt.contour(IG_Temp,IG_Press/1e5,tau_arr,levels=conlevels)
plt.clabel(CS, inline=1, fontsize=20)
cb=plt.colorbar()
cb.ax.tick_params(labelsize=20)
'''
#np.save('LLNL_aro_mech_IGPress',IG_Press)
#np.save('LLNL_aro_mech_IGTemp',IG_Temp)
np.save('LLNL_aro_mech_Tau_{}'.format(jobid),tau_result)
np.save('LLNL_aro_mech_FinalTemp_{}'.format(jobid),temp_result)
np.save('LLNL_aro_mech_Pres_{}'.format(jobid),pres_result)
#np.savefig('IgdelayLLNL')

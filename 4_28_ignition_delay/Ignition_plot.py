# -*- coding: utf-8 -*-
import sys
import numpy as np
import matplotlib.pyplot as plt

ig_press_cont=np.linspace(1e5,50e5,30)
low_res=np.array([400,500])
high_res=np.array(np.linspace(600,1000,30))
ig_temp_cont=np.concatenate((low_res,high_res),axis=0)  
tau_arr = np.zeros((np.size(ig_temp_cont),np.size(ig_press_cont)))
IG_Temp,IG_Press=np.meshgrid(ig_temp_cont,ig_press_cont,indexing='ij')  #Meshgrid for plotting 
# read from the out files
for jobid in range(30):
    curr_tau = np.load('tau_dat/LLNL_aro_mech_Tau_{}.npy'.format(jobid))
    tau_arr[:,jobid] = curr_tau

IG_Temp,IG_Press=np.meshgrid(ig_temp_cont,ig_press_cont,indexing='ij')  #Meshgrid for plotting        

np.save('LLNL_aro_mech_IGPress',IG_Press)
np.save('LLNL_aro_mech_IGTemp',IG_Temp)
np.save('LLNL_aro_mech_Tau',tau_arr)
print IG_Temp.shape
'''
conlevels=np.arange(1e-3,10e-3,1e-3)
plt.figure
plt.rcParams.update({'font.size': 30})
CS=plt.contour(IG_Temp,IG_Press/1e5,tau_arr,levels=conlevels)
plt.clabel(CS, inline=1, fontsize=20)
cb=plt.colorbar()
cb.ax.tick_params(labelsize=20)
'''
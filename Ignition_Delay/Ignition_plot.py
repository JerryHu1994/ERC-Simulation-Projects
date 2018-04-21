# -*- coding: utf-8 -*-
import sys
import numpy as np
import matplotlib.pyplot as plt

ig_temp_cont, ig_press_cont = 32, 30
out/Ignition_Delay_$(ProcId).out)
tau_arr = np.zeros((np.size(ig_temp_cont),np.size(ig_press_cont)))
Final_temp=np.zeros((np.size(ig_temp_cont),np.size(ig_press_cont)))

# read from the out files
for jobid in range(ig_temp_cont*ig_press_cont):
    file_name = "out/Ignition_Delay_{}.out)".format(jobid)
    with open("file_name") as f:
        lines = f.readlines()
        curr_temp = (float)lines[1]
        curr_tau = (float)lines[2]
        # populate tau into numpy array
        Final_temp[jobid/ig_temp_cont,jobid%ig_temp_cont] = curr_temp
        tau_arr[jobid/ig_temp_cont,jobid%ig_temp_cont] = curr_tau

IG_Temp,IG_Press=np.meshgrid(ig_temp_cont,ig_press_cont,indexing='ij')  #Meshgrid for plotting        

conlevels=np.arange(1e-3,10e-3,1e-3)
plt.figure
plt.rcParams.update({'font.size': 30})
CS=plt.contour(IG_Temp,IG_Press/1e5,tau_arr,levels=conlevels)
plt.clabel(CS, inline=1, fontsize=20)
cb=plt.colorbar()
cb.ax.tick_params(labelsize=20)

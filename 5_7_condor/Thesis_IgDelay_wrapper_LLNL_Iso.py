# -*- coding: utf-8 -*-
""" This code runs the ignition delay calcs for the thesis plots
Created on Thu May  3 12:21:03 2018

@author: agilliam2
"""
from Ignition_Delay_Temp_ALG_CONDOR_func import CV_IgDelay_Thesis

import sys
import numpy as np
import cantera as ct
#import matplotlib.pyplot as plt
import csv
import datetime
import time
import h5py
# from scipy.interpolate import interp1d 
import math
#from openpyxl import load_workbook


# handle the arguemnts
if len(sys.argv) != 2:
    print ("Error: Must have a jobid arguement\nUsage: python Thesis_IgDelay_wrapper_LLNL_Iso.py jobid")
    exit(1)
jobid = (int)(sys.argv[1])

#plt.rcParams["font.family"] = "Times New Roman" #Set Font Family to Times New Roman

"""==================================LLNL Data============================="""
"""-------------------------Iso-octane---------------------------"""
#filepath='E:\\UW_Madison_Research\\Data\\Oak_Ridge_Summer\\LNF\\Time_Based\\2017_07_11_isooctane_1000rpm_intake_sweep\\data_processed'
#filepath='E:\\UW_Madison_Research\Data\\Oak_Ridge_Summer\\LNF\\Time_Based\\2017_07_10_isooctane_2000rpm\\data_processed'
#f = h5py.File(filepath+'\\IsoOctane_run28_CrankAnalysis.mat', 'r')
"""Species and Indices"""
SpeciesFile=np.load('20180421_01-16.53_Iso_1000rpm_Wiebe_365.npz')


X=SpeciesFile['species']
CA=SpeciesFile['outdat'][:,0]
P=SpeciesFile['outdat'][:,1]*1e5
T=SpeciesFile['outdat'][:,5]
#EvalIndices=IndicesFile['CV_indices'][:] 
#EvalIndices=EvalIndices-1 #Derived From Matlab. Have to Subtract 1
EvalIndices=range(np.size(CA))
fname='Iso_1000_CONDOR.XLSX'

Temp=T[int(EvalIndices[1])]
Press=P[int(EvalIndices[1])]
PureFlag=0
RK_flag=0

Tau_mix=np.zeros((np.size(EvalIndices),1)); FinalTemp=np.zeros((np.size(EvalIndices),1));
Tau_Iso_LLNL=np.zeros((np.size(EvalIndices),1)); FinalTemp_Iso_LLNL=np.zeros((np.size(EvalIndices),1));
Crank_Points=np.zeros((np.size(EvalIndices),1));


loopsize = 57
start = jobid*loopsize
end = start + loopsize - 1
subloop = np.linspace(start, end, loopsize)
print ("starting index: {}".format(int(start)))
print ("ending index: {}".format(int(end)))
for i in subloop:
	i = int(i)
    if np.remainder(i,380)<1e-8:
        print('At Crank Angle'+str(CA[i]))
    x_current=X[int(EvalIndices[i]),:]
    Temp=T[int(EvalIndices[i])]
    Press=P[int(EvalIndices[i])]
    [Tau_mix[i], FinalTemp[i]]=CV_IgDelay_Thesis(x_current,Temp,Press,PureFlag,fname,RK_flag)
    [Tau_Iso_LLNL[i], FinalTemp_Iso_LLNL[i]]=CV_IgDelay_Thesis(x_current,Temp,Press,1,fname,RK_flag)

Crank_Points=CA#[EvalIndices.astype(int)]

"""Plot Ignition Delays vs. Crank Angle"""
'''
fig=plt.figure(figsize=(6.4,5.4))
ax=fig.gca()
plt.plot(Crank_Points,Tau_mix*1.e3,'-',label='Charge Composition')
plt.plot(Crank_Points,Tau_Iso_LLNL*1.e3,'-',label='Pure Iso-octane and air')
ax.grid(linestyle=':')
plt.xlabel('Crank Angle',fontsize=20)
plt.ylabel('Ignition Delay [ms]',fontsize=20)
plt.tick_params(labelsize=15)
plt.legend(fancybox="true")
'''
save_name = 'Iso_1000_90C_IgDel_Comparison_Full_CA_%d'%jobid
np.savez(save_name,mix_Tau=Tau_mix, pure_Tau=Tau_Iso_LLNL,Crank_Angle=CA)

#plt.savefig('Iso_1000_160C_IgDel_Comparison_Full_CA', dpi=600, facecolor='w', edgecolor='w',
#        orientation='portrait', papertype=None, format=None,
#        transparent=False, bbox_inches=None, pad_inches=0.05,
#        frameon=None)
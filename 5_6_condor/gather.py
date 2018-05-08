# -*- coding: utf-8 -*-
import sys
import numpy as np

'''
This file gathers all npz together.
'''
SpeciesFile=np.load('20180422_18-13.10_Aro_2000rpm_step4_CONDOR_395.npz')

CA=SpeciesFile['outdat'][:,0]
EvalIndices=range(np.size(CA))

# initialize container
Tau_mix=np.zeros((np.size(EvalIndices),1))
Tau_Iso_RK=np.zeros((np.size(EvalIndices),1))
Crank_Points=np.zeros((np.size(EvalIndices),1));

for i in range(40):
	start,end = i*57, i*57+56
	file_name = 'Aro_2000_160C_IgDel_Comparison_Full_CA_%d'%i
	curr_file = np.load(file_name)

	# copy tau mix
	curr_tau_mix[start:end,:] = curr_file['mix_Tau'][start:end,:]
	# copy tau iso
	curr_tau_iso_rk[start:end,:] = curr_file['pure_Tau'][start:end,:]

np.savez(save_name,mix_Tau=Tau_mix, pure_Tau=Tau_Iso_RK,Crank_Angle=Crank_Points)
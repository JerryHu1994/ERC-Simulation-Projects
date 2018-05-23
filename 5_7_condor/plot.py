#!/usr/bin/env python
##################################
# University of Wisconsin-Madison
# Author: Jieru Hu
##################################

import numpy as np
import matplotlib.pyplot as plt

SpeciesFile=np.load('20180421_01-16.53_Iso_1000rpm_Wiebe_365.npz')
Crank_Points=SpeciesFile['outdat'][:,0]


data = np.load('Iso_1000_90C_IgDel_Comparison_Full_CA.npz')
Tau_mix = data['mix_Tau']
Tau_Iso_LLNL = data['pure_Tau']

fig=plt.figure(figsize=(6.4,5.4))
ax=fig.gca()
plt.plot(Crank_Points,Tau_mix*1.e3,'-',label='Charge Composition')
plt.plot(Crank_Points,Tau_Iso_LLNL*1.e3,'-',label='Pure Iso-octane and air')
ax.grid(linestyle=':')
plt.xlabel('Crank Angle',fontsize=20)
plt.ylabel('Ignition Delay [ms]',fontsize=20)
plt.tick_params(labelsize=15)
plt.legend(fancybox="true")
plt.show()

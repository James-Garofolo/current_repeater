# file used to visualize signal behaviors of ideal spiking neural networks


# import libraries
import math
import numpy as np
import matplotlib.pyplot as plt

# time and data inputs
tstep = 0.000001
time = np.arange(0, 0.005, tstep)
din = 0.02
w = 0.9

# circuit characteristics
Rm = 100 # 100 ohms
Cm = 0.000001 # 1uF
Tm = Rm * Cm # decay constant, pretty much picked at random
Vl = 1 # reset voltage
Vth = 3 # spike voltage
Vc = 2 # center voltage

# signals
rst = False
Vm = np.ones_like(time) * Vc
spk = np.zeros_like(time)

# calculate the LIF voltage and spikes using a discrete version of Eq. 2.4 from Neuromorphic Photonics
i = 0
for t in time:
    if t: # just do this so Vm starts at 0
        if rst: # if we just spiked, decay back to Vl
            Vm[i] = Vm[i-1] - ((Vm[i-1]/Tm)*tstep) # accept no excitory input or pumping current
            if Vm[i] <= Vl:
                rst = False # start accepting input again
        else:
            Vm[i] = Vm[i-1] + (((Vc/Tm) - (Vm[i-1]/Tm) + (din/Cm))*tstep)  # use din for excitory input
            if Vm[i] >= Vth:
                spk[i] = 1
                rst = True # stop accepting excitory input until we hit Vl
    
    i += 1
    
# next neuron's signals
rst = False
Vm2 = np.ones_like(time) * Vc
spk2 = np.zeros_like(time)

# repeat the process using the previous neuron's outputs as inputs
i = 0
for t in time:
    if t: # just do this so Vm starts at 0
        if rst: # if we just spiked, decay back to Vl
            Vm2[i] = Vm2[i-1] - ((Vm2[i-1]/Tm)*tstep) # accept no excitory input or pumping current
            if Vm2[i] <= Vl:
                rst = False # start accepting input again
        else:
            Vm2[i] = Vm2[i-1] + (((Vc/Tm) - (Vm2[i-1]/Tm) + (w*spk[i]/Cm))*tstep)  # use weighted spike for excitory input
            if Vm2[i] >= Vth:
                spk2[i] = 1
                rst = True # stop accepting excitory input until we hit Vl

    i += 1

plt.plot(time, Vm, 'r-', label='Vm')
plt.plot(time, spk, 'b-', label='spk')
plt.plot(time, Vm2, 'g-', label='Vm2')
plt.plot(time, spk2, 'y-', label='spk2')
plt.title("I(t) = " + str(din) + ", w = " + str(w))
plt.legend()
plt.show()

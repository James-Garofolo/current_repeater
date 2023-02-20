import numpy as np
import math
import random
import matplotlib.pyplot as plt

sample = True
sample_t = 0
sample_c = 0.0000000005 #0.5nF
latch = False
latch_c = 0.0000000001 #0.1nF
latch_r = 1 # 1 Ohm
drain = False
drain_r = 1 # 1 Ohm

t_step = 0.000000000001
time = np.arange(0, 0.00000002, t_step)
i_in = np.ones_like(time) * random.randint(0, 10) * 0.1    
sample_v = np.zeros_like(time)
hold_v = np.zeros_like(time)

for t in range(1, len(time)):
    #i_in[t] += 0.1*math.sin(2*math.pi*5000000000*time[t])
    if sample:
        hold_v[t] = hold_v[t-1] # stay constant
        sample_v[t] = sample_v[t-1] + (i_in[t] * t_step)/sample_c # time average the current
        sample_t += t_step # count up sample time
        if sample_t >= sample_c: # check sample period
            sample = False
            latch = True
            sample_t = 0

    elif latch:
        sample_v[t] = sample_v[t-1] # stay constant
        hold_v[t] = hold_v[t-1] + ((sample_v[t-1] - hold_v[t-1])*t_step)/(latch_c*latch_r) # move towards sample_v

        if abs(hold_v[t] - sample_v[t]) < 0.000001: # if the two voltages are about the same
            latch = False
            drain = True

    elif drain:
        hold_v[t] = hold_v[t-1] # stay constant
        sample_v[t] = sample_v[t-1] - ((sample_v[t-1])*t_step)/(drain_r*sample_c) # drain sample cap

        if sample_v[t] < 0.000001: # if sample cap is about at 0V
            i_in[t] = random.randint(0, 10) * 0.1 
            for a in range(t+1, len(time)):
                i_in[a] = i_in[t] 
            drain = False
            sample = True


plt.plot(time*pow(10,9), hold_v, 'r-', label="Vhold")
plt.plot(time*pow(10,9), sample_v, 'b-', label="Vsample")
plt.plot(time*pow(10,9), i_in, 'g--', label="Iin")
plt.legend()
plt.title("Latching of Random Currents")
plt.xlabel("Time (ns)")
plt.ylabel("Voltage/Current")
plt.show()








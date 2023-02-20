import matplotlib.pyplot as plt
import scipy.signal as sig
import numpy as np
import os

time = []
v_sample = []
i_in = []
v_latched = []
i_out = []
thing = True
arr = np.loadtxt(os.getcwd() + "/data/redo.csv", delimiter=",").T
start = arr[0,520]
for t in range(len(arr[0])):
    arr[0,t] -= start
    if (arr[0,t] > 0) and (arr[0,t] < 1):
        if thing:
            print(t)
            thing = False
        time.append(arr[0,t])
        v_sample.append(arr[1,t])
        i_in.append(arr[2,t])
        v_latched.append(arr[3,t])
        i_out.append(arr[4,t])


#print(arr[0])
#print('\n\n', (1/(arr[0,1]-arr[0,0])), '\n\n')
#b, a = sig.butter(5, 2000, fs=(1/(arr[0,1]-arr[0,0])))
#w, h = sig.freqz(b, a)
#b = np.fft.fft(a[1])
#freq = np.fft.fftfreq(a[0].size, d=(a[0,1]-a[0,0]))

#Iin = sig.lfilter(b, a, arr[2])
#Vs = sig.lfilter(b, a, arr[1])
#Vl = sig.lfilter(b, a, arr[3])
#Iout = sig.lfilter(b, a, arr[4])

#plt.plot(w, h)
#plt.plot(arr[0], Iin, label="Iin")
#plt.plot(arr[0], Vl, label="Vlatch")
#plt.plot(arr[0], Iout, label="Iout")
#plt.plot(arr[0], Vs, label="Vsample")

#plt.plot(arr[0], arr[2], label="Iin")
#plt.plot(arr[0], arr[3], label="Vlatch")
#plt.plot(arr[0], arr[4], label="Iout")
#plt.plot(arr[0], arr[1], label="Vsample")

plt.plot(time, i_in, label="Iin * 100")
plt.plot(time, v_latched, label="Vlatch")
plt.plot(time, i_out, label="Iout * 100")
plt.plot(time, v_sample, label="Vsample")

plt.legend(loc='upper left')
plt.title("Latching of Random Currents")
plt.xlabel("Time (s)")
plt.ylabel("Voltage/Current")
#plt.ylim(top=0.4)
plt.show()
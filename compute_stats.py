import matplotlib.pyplot as plt
import numpy as np
import os
import math

print("\n\n")

arr = np.loadtxt(os.getcwd() + "/data/redo_long.csv", delimiter=",").T

time = []
v_sample = []
i_in = []
i_out = []
heartbeat = []
sample_error = []
output_error = []
o_current_level = []
s_current_level = []
start = 0
durations = []
state = True
count = 0

for t in range(len(arr[0])):
    time.append(arr[0,t] - arr[0,0])
    v_sample.append(arr[1,t])
    i_in.append(arr[2,t])
    i_out.append(arr[3,t])
    heartbeat.append(arr[4,t])

    if state:
        if heartbeat[t] > 4:
            state = False
            sample_error.append((v_sample[t]-i_in[t])/i_in[t])
            s_current_level.append(i_in[t])
            start = time[t]

    else:
        if heartbeat[t] < 1:
            state = True
            output_error.append((i_out[t]-i_in[t])/i_in[t])
            o_current_level.append(i_in[t])
            durations.append(time[t] - start)
            

print(len(sample_error), len(output_error))

qs = np.quantile(sample_error, [0.25, 0.75])
for a in sample_error:
    if (a < qs[0] - 3*(qs[1]-qs[0])) or (a > qs[1] + 3*(qs[1]-qs[0])):
        count += 1
        sample_error.remove(a)
print("removed from sample:", count)
sample_mean = np.average(sample_error)
sample_stdev = np.std(sample_error)
sample_range = (1.96*sample_stdev/math.sqrt(len(sample_error)))
print("sample guy: ", sample_mean, sample_stdev, sample_range)#, s_r[0,1])

count = 0
qs = np.quantile(output_error, [0.25, 0.75])
for a in output_error:
    if (a < qs[0] - 3*(qs[1]-qs[0])) or (a > qs[1] + 3*(qs[1]-qs[0])):
        count += 1
        output_error.remove(a)
print("removed from output:", count)

output_mean = np.average(output_error)
output_stdev = np.std(output_error)
output_range = (1.96*output_stdev/math.sqrt(len(output_error)))
print("output guy: ", output_mean, output_stdev,  output_range)#, o_r[0,1])

count = 0
qs = np.quantile(durations, [0.25, 0.75])
for a in durations:
    if (a < qs[0] - 3*(qs[1]-qs[0])) or (a > qs[1] + 3*(qs[1]-qs[0])):
        count += 1
        durations.remove(a)
print("removed from durations:", count)
time_mean = np.average(durations)
time_stdev = np.std(durations)
time_range = (1.65*time_stdev/math.sqrt(len(durations)))
less_than = time_mean + time_range

print("time guy:", time_mean, time_stdev, time_range, less_than)

#plt.hist(sample_mean)
#plt.hist(output_mean)
#plt.ylabel("Probability density")
#plt.xlabel("Percentage error")
#plt.plot(time, v_sample, label="Vs")
#plt.plot(time, i_in, label="Iin")
#plt.plot(time, i_out, label="Iout")
#plt.plot(time, check_sample, label="sample check")
#plt.plot(time, check_out, label="out check")
fig, a1 = plt.subplots(1, 1)
a1.hist(sample_error, 20, label='sample')
a1.hist(output_error, 20, label='out')
#plt.plot(s_current_level, sample_error)
plt.legend()
plt.show()


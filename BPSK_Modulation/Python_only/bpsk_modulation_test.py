import numpy as np; r_, pi = np.r_, np.pi
from numpy.random import random as rand
import matplotlib.pyplot as plt


##Function for creating random BPSK symbols
def rand_BPSK(num_sym):
    x = rand(num_sym)
    x = np.floor(2*x)  #bit stream
    x = 2*x - 1 #symbol mapping 0 ->-1V, 1->+1V
    return x
    

## Upsampling Factor, and Sampling Rates
#Upsample factor 
M = 10  

fs = 500 #original sampling frequency in Hz (symbol rate)
fs_new = fs*M #new sampling frequency (5kHz) (samples that mix w/ carrier)


## Generate 100 random symbols
num_sym = 100
x_sym = rand_BPSK(num_sym)

# Now plot the results
plt.figure("From Python")
plt.subplot(221)
num_pts = 50
plt.stem(x_sym[:num_pts]), plt.grid(1)
plt.ylim(-1.5, 1.5)
plt.title("Symbols")
plt.xlabel('Time'), plt.ylabel('Magnitude')

## Upsample digital signal

# create upsampled signal
# by repeating each element M times
x_n = np.tile( x_sym, [M,1] ).flatten('F')

# x[n] is our discrete time signal (which will go through DAC)
plt.subplot(223)
plt.plot(x_n[:num_pts*M]), plt.grid(1)
plt.ylim(-1.5, 1.5)
plt.title("Upsampled Baseband")
plt.xlabel('Time'), plt.ylabel('Magnitude')

#Note: symbol rate (i.e. x_sym) was generated at 500 symbol/sec (500Hz)
#After upsampling, our sample rate is 5kHz
#Max freq of signals we create is (sample rate/2)

## Simulate Carrier Frequency
fc = 0.2 * fs_new/2 #carrier freq -> certain percentage of fs_new/2
n = r_[0: x_n.size] #time index
cos_wave = np.cos(2*pi*fc/fs_new * n)
plt.subplot(222)
plt.plot(cos_wave[:100]), plt.grid(1)
plt.title("Carrier Wave")
plt.xlabel('Time'), plt.ylabel('Magnitude')

## Simulate Mixing and TX
s_t = x_n * cos_wave
plt.subplot(224)
plt.plot(s_t[:100]), plt.grid(1)
plt.title("TX (Modulated) Signal")
plt.xlabel('Time'), plt.ylabel('Magnitude')
plt.tight_layout()

plt.show()
## Save Plot
# plt.savefig("BPSK Modulation Sim1.png", dpi=300)









#-------------------------------------------------------------
#-------------------------------------------------------------
# Import Various Modules

# Modules for getting path of this file
from inspect import getsourcefile 
from os.path import abspath, dirname 

# Module for changing working directory
import os

# Module for running shell commands
import subprocess as spr

# Module for arrays and plotting
import numpy as np; r_ = np.r_
import matplotlib.pyplot as plt
# plt.ion()
# plt.close('all')

# Time Module (just in case)
import time
#-------------------------------------------------------------
#-------------------------------------------------------------
# In/Out files

cppfile = "bpsk_mod"
outfile = "data.csv" # name of file

# Get path of this Python file
# The cpp program should be in same directory
path = dirname( abspath( getsourcefile(lambda:0) ) )

# Change the working directory, and print
os.chdir(path)
print("The current Working Directory is:")
spr.run("pwd")  
#-------------------------------------------------------------
#-------------------------------------------------------------
# Compile and run the cpp file
# If already this was done separately,
# then this section is optional

spr.run(["g++", cppfile + ".cpp", "-o", cppfile])
spr.run(["./" + cppfile, outfile])

# Make sure output file exists
while not os.path.exists(outfile):
    time.sleep(1)
#-------------------------------------------------------------
#-------------------------------------------------------------
# The Cpp program has created the outfile
# Now read that file

f1 = open(outfile, 'r')
data = [] # An empty list for storing data
for k in f1:
    k = k.replace("\n", "") # Get rid of newline character
    if k[-1]==",":
        k = k[:-1]
    line = k.split(",")
    data.append(line)
    # print(k)
f1.close()
#-------------------------------------------------------------
#-------------------------------------------------------------
# Now we have the data
# Convert to numpy arrays

x_bits    = np.loadtxt(data[0], dtype = 'int')    # bits
x_sym     = np.loadtxt(data[1], dtype = 'int')    # symbols
x_n       = np.loadtxt(data[2], dtype = 'int')    # Upsampled symbols
cos_wave  = np.loadtxt(data[3], dtype = 'float')  # Carrier Wave
s_t       = np.loadtxt(data[4], dtype = 'float')  # Tx Signal (Analog Simulation)

# DEBUG
# print("Percentage of 1's = ", x_bits.sum() / x_bits.size)
#-------------------------------------------------------------
#-------------------------------------------------------------
# Plot Data Symbols
plt.figure("From C++ Data")
plt.subplot(221)
num_pts = 50
M = 10 #Upsampling factor
plt.stem(r_[0:num_pts], x_sym[:num_pts]), plt.grid(1)
plt.ylim(-1.5, 1.5)
plt.title("Symbols")
plt.xlabel('Time'), plt.ylabel('Magnitude')

# Plot Upsampled Symbols
plt.subplot(223)
plt.plot(x_n[:num_pts*M]), plt.grid(1)
plt.ylim(-1.5, 1.5)
plt.title("Upsampled Baseband")
plt.xlabel('Time'), plt.ylabel('Magnitude')

# Simulate Carrier Frequency
plt.subplot(222)
plt.plot(cos_wave[:100]), plt.grid(1)
plt.title("Carrier Wave")
plt.xlabel('Time'), plt.ylabel('Magnitude')

plt.subplot(224)
plt.plot(s_t[:100]), plt.grid(1)
plt.title("TX (Modulated) Signal")
plt.xlabel('Time'), plt.ylabel('Magnitude')

plt.tight_layout()
plt.show()








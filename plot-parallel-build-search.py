import sys, getopt
import matplotlib
#matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt
import csv
import datetime
import subprocess
import shlex
import math
import pandas as pd 
import numpy as np

try:
    opts, args = getopt.getopt(sys.argv,"hi:o:")
except getopt.GetoptError:
    print("parallel-build-script.py -p <no of processors>")
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print("parallel-build-script.py -p <no of processors>")
        sys.exit()
    elif opt == '-p':
        print(arg)
noOfProcessors = 8
print(str(sys.argv), noOfProcessors)
processors = [str(2**i) for i in range(0, int(math.log(noOfProcessors,2)) + 1)]
print("processors::" , processors)

now = datetime.datetime.now()
print ("Current date and time : ")
print (now.strftime("%Y-%m-%d"))
day = now.strftime("%Y-%m-%d")

programs = ["parallelPreProcessInt", "parallelPreProcessLong"]
shortPrograms = {"parallelPreProcessInt":"int", "parallelPreProcessLong":"long"}
header = "N,node size,build horizontal(s),build vertical(s),seq search(s),Binary search(s)\n"
pwd = subprocess.run('pwd',stdout=subprocess.PIPE, universal_newlines=True).stdout[:-1]
programPath = pwd + '/'
filePath = pwd + "/timePerformance" 
print(filePath)

print(programPath)

itemSize = [2**25, 2**26, 2**27]
parallelData = []
sheets = []
fileNames = []
for N in itemSize: #3
    for program in programs: #2
        for processor in processors: #4        
            fileName = filePath + "/"+ day + "-" +program + processor + "-" + str(N) +  "-time.csv"
            sheets = sheets + [fileName]
            fileNames = fileNames + ["N = 2^" + str(int(math.log(N,2))) + " " + shortPrograms[program] + ", P = " + processor]

dfs = [pd.read_csv(sheet, sep=",", index_col=False) for sheet in sheets]

fig, ax = plt.subplots()
cols = dfs[0].keys()
cols = cols[2:]
print(cols)
#https://thispointer.com/pandas-change-data-type-of-single-or-multiple-columns-of-dataframe-in-python/
nodeSizes = np.array([1,4, 8, 16, 32, 64, 128, 256, 512])

index= 0
for N in itemSize:
    for col in cols:
        print(col)
        fig, ax = plt.subplots()
        for i in range(index, index + 4):
            #dfs[i]['node size'] = pd.to_numeric(dfs[i]['node size']).astype('int')
            line, = ax.plot(nodeSizes, dfs[i][col], label = fileNames[i])
        ax.legend(loc='upper right')
        plt.xlabel('nodes sizes')
        plt.ylabel('time(s)')
        plt.title(col + " of 2^" + str(int(math.log(N,2))) + " int "+ " in parallel")
        plt.show()
        fig, ax = plt.subplots()
        for i in range(index + 4, index + 8):
            #dfs[i]['node size'] = pd.to_numeric(dfs[i]['node size']).astype('int')
            line, = ax.plot(nodeSizes, dfs[i][col], label = fileNames[i])
        ax.legend(loc='upper right')
        plt.xlabel('nodes sizes')
        plt.ylabel('time(s)')
        plt.title(col + " of 2^" + str(int(math.log(N,2))) + " long "+ " in parallel")
        plt.show()
    index = index + 8
    
#Plot different N for int and long
for i in range(0,8):
    for col in cols:
        print(col)
        fig, ax = plt.subplots()
        line1, = ax.plot(nodeSizes, dfs[i][col], label = fileNames[i])
        line2, = ax.plot(nodeSizes, dfs[i+8][col], label = fileNames[i+8])   
        line3, = ax.plot(nodeSizes, dfs[i+16][col], label = fileNames[i+16]) 
        ax.legend(loc='upper right')    
        plt.xlabel('nodes sizes')
        plt.ylabel('time(s)')
        plt.title(col + " with different sizes"+ " in parallel")
        plt.show()

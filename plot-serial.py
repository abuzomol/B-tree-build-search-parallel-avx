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

now = datetime.datetime.now()
print ("Current date and time : ")
print (now.strftime("%Y-%m-%d"))
day = now.strftime("%Y-%m-%d")

programs = ["seqBuildSearchInt", "seqBuildSearchLong",
            "seqBuildSearchFloat", "seqBuildSearchDouble"]
shortPrograms = {"seqBuildSearchInt":"int", "seqBuildSearchLong":"long",
            "seqBuildSearchFloat":"float", "seqBuildSearchDouble":"double"}
header = "N,node size,build horizontal(s),build vertical(s),seq search(s),binary search(s), simd search(s)\n"
headerTokens = header.split(",")
pwd = subprocess.run('pwd',stdout=subprocess.PIPE, universal_newlines=True).stdout[:-1]
filePath = pwd + "/data/"
print(filePath)
fileSave = pwd + "/figures/"
itemSize = [2**25, 2**26, 2**27]
seqData = []
sheets = []
fileNames = []

for N in itemSize: #3
    for program in programs: #4
        fileName = filePath + program + "-" + str(N) +  ".csv"
        sheets = sheets + [fileName]
        fileNames = fileNames + ["N = 2^" + str(int(math.log(N,2))) + " " + shortPrograms[program]]
[print(sheet) for sheet in sheets]
dfs = [pd.read_csv(sheet, sep=",", index_col=False, names = list(range(0,9))) for sheet in sheets]

fig, ax = plt.subplots()
cols = dfs[0].keys()
cols = [int(col) for col in cols]
cols = cols[2:7] #excludes the first two columns
print(cols)
# some notes taken from https://thispointer.com/pandas-change-data-type-of-single-or-multiple-columns-of-dataframe-in-python/
nodeSizes = [8*i for i in range(1, 65)]
    
# Plot same type different N for int, long, double and float
print("dfs length:",len(dfs))
types=['int','long','float','double']
for i in range(0,4):
    for col in cols:
        j = 0
        fig, ax = plt.subplots()
        line1, = ax.plot(nodeSizes, dfs[i+j][col][1:], label = fileNames[i+j])
        j = 4
        line2, = ax.plot(nodeSizes, dfs[i+j][col][1:], label = fileNames[i+j])   
        j = 8
        line3, = ax.plot(nodeSizes, dfs[i+j][col][1:], label = fileNames[i+j]) 
        ax.legend(loc='upper right')
        plt.xlabel('nodes sizes')
        plt.ylabel('time(s)')
        plt.title("serial " + headerTokens[col] + " with different N sizes")
        plt.yticks([],[])
        ax.set_yticks([], minor=True)
        plt.savefig(fileSave + "serial-" +headerTokens[int(col)] + "-same-type-different-sizes-" + types[i])

#Plot same N different types
# for N in itemSize:
#     for col in cols:
#         print(col)
#         fig, ax = plt.subplots()
#         for i in range(4):
#             #dfs[i]['node size'] = pd.to_numeric(dfs[i]['node size']).astype('int')
#             line, = ax.plot(nodeSizes, dfs[i][col][1:], label = fileNames[i])
#         ax.legend(loc='upper right')
#         plt.xlabel('nodes sizes')
#         plt.ylabel('time(s)')
#         plt.title(headerTokens[col] + " of 2^" + str(int(math.log(N,2))))
#         plt.show()
#Plot same N two builds and different search
for N in itemSize:
    for type in types:
        fig, ax = plt.subplots()
        #dfs[i]['node size'] = pd.to_numeric(dfs[i]['node size']).astype('int')
        line1, = ax.plot(nodeSizes, dfs[i][cols[0]][1:], label = headerTokens[cols[0]] )
        line2, = ax.plot(nodeSizes, dfs[i][cols[1]][1:], label = headerTokens[cols[1]])
        ax.legend(loc='upper right')
        plt.xlabel('nodes sizes')
        plt.ylabel('time(s)')
        plt.title( "build a tree" + " of 2^" + str(int(math.log(N,2))) + " " + type)
        plt.yticks([],[])
        ax.set_yticks([], minor=True)
        plt.show()
        fig, ax = plt.subplots()
        #dfs[i]['node size'] = pd.to_numeric(dfs[i]['node size']).astype('int')
        line1, = ax.plot(nodeSizes, dfs[i][cols[2]][1:], label = headerTokens[cols[2]] )
        line2, = ax.plot(nodeSizes, dfs[i][cols[3]][1:], label = headerTokens[cols[3]])
        line3, = ax.plot(nodeSizes, dfs[i][cols[4]][1:], label = headerTokens[cols[4]])
        ax.legend(loc='upper right')
        plt.xlabel('nodes sizes')
        plt.ylabel('time(s)')
        plt.title( "build a tree" + " of 2^" + str(int(math.log(N,2))) + " " + type)
        plt.yticks([],[])
        ax.set_yticks([], minor=True)
        plt.show()
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
figureLabels = []

#get all figure labels, and csv filenames
for N in itemSize: #3
    for program in programs: #4
        csvfileName = filePath + program + "-" + str(N) +  ".csv"
        sheets = sheets + [csvfileName]
        figureLabels = figureLabels + ["N = 2^" + str(int(math.log(N,2))) + " " + shortPrograms[program]]
[print(sheet) for sheet in sheets]
[print(label) for label in figureLabels]
#read all csv files into data frames
dfs = [pd.read_csv(sheet, sep=",", index_col=False, names = list(range(0,9))) for sheet in sheets]

fig, ax = plt.subplots()
cols = dfs[0].keys()
cols = [int(col) for col in cols] #list of columns 
cols = cols[2:7] #excludes the first two columns
print(cols)
# some notes taken from https://thispointer.com/pandas-change-data-type-of-single-or-multiple-columns-of-dataframe-in-python/
nodeSizes = [8*i for i in range(1, 65)]
    
#Plot same N two builds and 3 different search
for i in range(len(dfs)):
    fig, ax = plt.subplots()
    #dfs[i]['node size'] = pd.to_numeric(dfs[i]['node size']).astype('int')
    line1, = ax.plot(nodeSizes, dfs[i][cols[0]][1:], label = headerTokens[cols[0]] ) #horizontal build
    line2, = ax.plot(nodeSizes, dfs[i][cols[1]][1:], label = headerTokens[cols[1]]) #vertical build
    ax.legend(loc='upper left')
    plt.xlabel('nodes sizes')
    plt.ylabel('time(s)')
    plt.title("serial build comparisons " + figureLabels[i])
    plt.yticks([],[])
    ax.set_yticks([], minor=True)
    plt.savefig(fileSave + "serial-build-compare-"+figureLabels[i])
    fig, ax = plt.subplots()
    #dfs[i]['node size'] = pd.to_numeric(dfs[i]['node size']).astype('int')
    line1, = ax.plot(nodeSizes, dfs[i][cols[2]][1:], label = headerTokens[cols[2]] ) #sequential search
    line2, = ax.plot(nodeSizes, dfs[i][cols[3]][1:], label = headerTokens[cols[3]]) #binary search
    line3, = ax.plot(nodeSizes, dfs[i][cols[4]][1:], label = headerTokens[cols[4]]) #simd search
    ax.legend(loc='upper left')
    plt.xlabel('nodes sizes')
    plt.ylabel('time(s)')
    plt.title("serial search comparisons " + figureLabels[i])
    plt.yticks([],[])
    ax.set_yticks([], minor=True)
    plt.savefig(fileSave + "serial-search-compare-"+figureLabels[i])

# Plot same type different N for int, long, double and float
print("dfs length:",len(dfs))
types=['int','long','float','double']
for i in range(0,4):
    for col in cols:
        j = 0
        fig, ax = plt.subplots()
        line1, = ax.plot(nodeSizes, dfs[i+j][col][1:], label = figureLabels[i+j])
        j = 4
        line2, = ax.plot(nodeSizes, dfs[i+j][col][1:], label = figureLabels[i+j])   
        j = 8
        line3, = ax.plot(nodeSizes, dfs[i+j][col][1:], label = figureLabels[i+j]) 
        ax.legend(loc='upper left')
        plt.xlabel('nodes sizes')
        plt.ylabel('time(s)')
        plt.title("serial " + headerTokens[col] + " with different N sizes")
        plt.yticks([],[])
        ax.set_yticks([], minor=True)
        plt.savefig(fileSave + "serial-" + headerTokens[int(col)] + "-same-type-different-sizes-" + types[i])

#Plot same N same columns different types
for i in range(len(itemSize)):
    for col in cols:
        fig, ax = plt.subplots()
        for j in range(4):
            #dfs[i]['node size'] = pd.to_numeric(dfs[i]['node size']).astype('int')
            line, = ax.plot(nodeSizes, dfs[i*4+j][col][1:], label = types[j])
        ax.legend(loc='upper left')
        plt.xlabel('nodes sizes')
        plt.ylabel('time(s)')
        plt.yticks([],[])
        ax.set_yticks([], minor=True)
        plt.title(headerTokens[col] + " of 2^" + str(int(math.log(itemSize[i],2))))
        plt.savefig(fileSave + "serial-"+ headerTokens[col] + "-same-N"+ str(itemSize[i]))

#Plot fair comparisons, int and long, float and double
for col in cols:
    fig, ax = plt.subplots()
    line1, = ax.plot(nodeSizes, dfs[5][col][1:], label = types[1]) #long
    line2, = ax.plot(nodeSizes, dfs[8][col][1:], label = types[0]) #long
    ax.legend(loc='upper left')
    plt.xlabel('nodes sizes')
    plt.ylabel('time(s)')
    plt.yticks([],[])
    ax.set_yticks([], minor=True)
    plt.title(headerTokens[col] + " of 2^27*4 bytes as int and long")
    plt.savefig(fileSave + "serial-"+ headerTokens[col] + "-equiv-N"+ str(2**27) + "-int-long")
    fig, ax = plt.subplots()
    line1, = ax.plot(nodeSizes, dfs[7][col][1:], label = types[3]) #long
    line2, = ax.plot(nodeSizes, dfs[10][col][1:], label = types[2]) #long
    ax.legend(loc='upper left')
    plt.xlabel('nodes sizes')
    plt.ylabel('time(s)')
    plt.yticks([],[])
    ax.set_yticks([], minor=True)
    plt.title(headerTokens[col] + " of 2^27*4 bytes as float and double")
    plt.savefig(fileSave + "serial-"+ headerTokens[col] + "-equiv-N"+ str(2**27)+"-float-double")
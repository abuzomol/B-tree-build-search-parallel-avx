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
header = "N,node size,build horizontal(s),build vertical(s),seq search(s),binary search(s), simd search(s)"
headerTokens = header.split(",")
pwd = subprocess.run('pwd',stdout=subprocess.PIPE, universal_newlines=True).stdout[:-1]
filePath = pwd + "/experiments/data/"
print(filePath)
fileSave = pwd + "/experiments/figures/"
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
dfs = [pd.read_csv(sheet, sep=",", names = list(range(0,7))) for sheet in sheets]
dfs = [df[:][1:].apply(pd.to_numeric) for df in dfs]
for col in dfs[0].columns:
    print ('column', col,':', type(dfs[0][col][1]))
fig, ax = plt.subplots()
cols = dfs[0].keys()
cols = [int(col) for col in cols] #list of columns
cols = cols[2:7]
print("cols:",cols)
# some notes taken from https://thispointer.com/pandas-change-data-type-of-single-or-multiple-columns-of-dataframe-in-python/
nodeSizes = [8*i for i in range(1, 65)]
    
#Plot same N same type two builds and 3 different search
for i in range(len(dfs)):
    fig, ax = plt.subplots()
    #dfs[i]['node size'] = pd.to_numeric(dfs[i]['node size']).astype('int')
    line1, = ax.plot(nodeSizes, dfs[i][cols[0]], label = headerTokens[cols[0]] ) #horizontal build
    line2, = ax.plot(nodeSizes, dfs[i][cols[1]], label = headerTokens[cols[1]]) #vertical build
    # ax.legend(loc='upper right')
    plt.rcParams['figure.dpi'] = 360
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True,ncol=4)
    plt.xlabel('nodes sizes')
    ax.xaxis.set_label_coords(1.05, -0.025)
    plt.ylabel('time(s)')
    plt.title("serial build comparisons " + figureLabels[i])
    right_side = ax.spines["right"]
    right_side.set_visible(False)
    top_side = ax.spines["top"]
    top_side.set_visible(False)
    plt.savefig(fileSave + "serial-build-compare-"+figureLabels[i])
    fig, ax = plt.subplots()
    #dfs[i]['node size'] = pd.to_numeric(dfs[i]['node size']).astype('int')
    # print(figureLabels[i][9:])
    if figureLabels[i][9:] in ["int", "float"]:
        line1, = ax.plot(nodeSizes[1::2], dfs[i][cols[2]][1::2], label = headerTokens[cols[2]] ) #sequential search
        line2, = ax.plot(nodeSizes[1::2], dfs[i][cols[3]][1::2], label = headerTokens[cols[3]]) #binary search
        line3, = ax.plot(nodeSizes[1::2], dfs[i][cols[4]][1::2], label = headerTokens[cols[4]]) #simd search
    else:
        line1, = ax.plot(nodeSizes, dfs[i][cols[2]], label = headerTokens[cols[2]] ) #sequential search
        line2, = ax.plot(nodeSizes, dfs[i][cols[3]], label = headerTokens[cols[3]]) #binary search
        line3, = ax.plot(nodeSizes, dfs[i][cols[4]], label = headerTokens[cols[4]]) #simd search
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True,ncol=4)
    plt.xlabel('nodes sizes')
    ax.xaxis.set_label_coords(1.05, -0.025)
    plt.ylabel('time(s)')
    plt.title("serial search comparisons " + figureLabels[i])
    # plt.yticks([],[])
    # ax.set_yticks([], minor=True)
    # y_ticks = np.arange(0, 10, .5)
    # plt.yticks(y_ticks)
    plt.rcParams['figure.dpi'] = 360
    right_side = ax.spines["right"]
    right_side.set_visible(False)
    top_side = ax.spines["top"]
    top_side.set_visible(False)
    plt.savefig(fileSave + "serial-search-compare-"+figureLabels[i])

# Plot same type different N for int, long, double and float
print("dfs length:",len(dfs))
types=['int','long','float','double']
for i in range(0,4):
    for col in cols:
        if col < 6:
            j = 0
            fig, ax = plt.subplots()
            line1, = ax.plot(nodeSizes, dfs[i+j][col], label = figureLabels[i+j])
            j = 4
            line2, = ax.plot(nodeSizes, dfs[i+j][col], label = figureLabels[i+j])   
            j = 8
            line3, = ax.plot(nodeSizes, dfs[i+j][col], label = figureLabels[i+j]) 
        else:#SIMD
            j = 0
            fig, ax = plt.subplots()
            line1, = ax.plot(nodeSizes[1::2], dfs[i+j][col][1::2], label = figureLabels[i+j])
            j = 4
            line2, = ax.plot(nodeSizes[1::2], dfs[i+j][col][1::2], label = figureLabels[i+j])   
            j = 8
            line3, = ax.plot(nodeSizes[1::2], dfs[i+j][col][1::2], label = figureLabels[i+j]) 
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True,ncol=4)
        plt.xlabel('nodes sizes')
        ax.xaxis.set_label_coords(1.05, -0.025)
        plt.ylabel('time(s)')
        plt.title("serial " + headerTokens[col] + " with different N " + types[i])
        # plt.yticks([],[])
        # ax.set_yticks([], minor=True)
        plt.rcParams['figure.dpi'] = 360
        right_side = ax.spines["right"]
        right_side.set_visible(False)
        top_side = ax.spines["top"]
        top_side.set_visible(False)
        #sns.despine();
        plt.savefig(fileSave + "serial-" + headerTokens[int(col)] + "-same-type-different-sizes-" + types[i])

#Plot same N same columns different types
for i in range(len(itemSize)):
    for col in cols:
        fig, ax = plt.subplots()
        for j in range(4):
            #dfs[i]['node size'] = pd.to_numeric(dfs[i]['node size']).astype('int')
            line, = ax.plot(nodeSizes[1::2], dfs[i*4+j][col][1::2], label = types[j])
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True,ncol=4)
        plt.xlabel('nodes sizes')
        ax.xaxis.set_label_coords(1.05, -0.025)
        plt.ylabel('time(s)')
        # plt.yticks([],[])
        # ax.set_yticks([], minor=True)
        plt.title(headerTokens[col] + " of 2^" + str(int(math.log(itemSize[i],2))) + " of ints longs floats & doubles" )
        plt.rcParams['figure.dpi'] = 360
        right_side = ax.spines["right"]
        right_side.set_visible(False)
        top_side = ax.spines["top"]
        top_side.set_visible(False)
        plt.savefig(fileSave + "serial-"+ headerTokens[col] + "-same-N"+ str(itemSize[i]))

#Plot fair comparisons, int and long, float and double except simd
for col in [2,3,4,5]:
    fig, ax = plt.subplots()
    line1, = ax.plot(nodeSizes, dfs[5][col], label = types[1]) 
    line2, = ax.plot(nodeSizes, dfs[8][col], label = types[0]) 
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True,ncol=4)
    plt.xlabel('nodes sizes')
    ax.xaxis.set_label_coords(1.05, -0.025)
    plt.ylabel('time(s)')
    # plt.yticks([],[])
    # ax.set_yticks([], minor=True)
    plt.title(headerTokens[col] + " of 2^27*4 bytes as int and long")
    plt.rcParams['figure.dpi'] = 360
    right_side = ax.spines["right"]
    right_side.set_visible(False)
    top_side = ax.spines["top"]
    top_side.set_visible(False)
    plt.savefig(fileSave + "serial-"+ headerTokens[col] + "-equiv-N"+ str(2**27) + "-int-long")
    fig, ax = plt.subplots()
    line1, = ax.plot(nodeSizes, dfs[7][col], label = types[3]) 
    line2, = ax.plot(nodeSizes, dfs[10][col], label = types[2]) 
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True,ncol=4)
    plt.xlabel('nodes sizes')
    ax.xaxis.set_label_coords(1.05, -0.025)
    # plt.ylabel('time(s)')
    # plt.yticks([],[])
    ax.set_yticks([], minor=True)
    plt.title(headerTokens[col] + " of 2^27*4 bytes as float and double")
    plt.rcParams['figure.dpi'] = 360
    right_side = ax.spines["right"]
    right_side.set_visible(False)
    top_side = ax.spines["top"]
    top_side.set_visible(False)
    plt.savefig(fileSave + "serial-"+ headerTokens[col] + "-equiv-N"+ str(2**27)+"-float-double")
#plot simd operations
simd = 6
fig, ax = plt.subplots()
line1, = ax.plot(nodeSizes[1::2], dfs[5][simd][1::2], label = types[1]) 
line2, = ax.plot(nodeSizes[1::2], dfs[8][simd][1::2], label = types[0]) 
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
        fancybox=True, shadow=True,ncol=4)
plt.xlabel('nodes sizes')
ax.xaxis.set_label_coords(1.05, -0.025)
plt.ylabel('time(s)')
# plt.yticks([],[])
# ax.set_yticks([], minor=True)
plt.title(headerTokens[simd] + " of 2^27*4 bytes as int and long")
plt.rcParams['figure.dpi'] = 360
right_side = ax.spines["right"]
right_side.set_visible(False)
top_side = ax.spines["top"]
top_side.set_visible(False)
plt.savefig(fileSave + "serial-"+ headerTokens[simd] + "-equiv-N"+ str(2**27) + "-int-long")
fig, ax = plt.subplots()
line1, = ax.plot(nodeSizes[1::2], dfs[7][simd][1::2], label = types[3]) 
line2, = ax.plot(nodeSizes[1::2], dfs[10][simd][1::2], label = types[2]) 
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
        fancybox=True, shadow=True,ncol=4)
plt.xlabel('nodes sizes')
ax.xaxis.set_label_coords(1.05, -0.025)
# plt.ylabel('time(s)')
# plt.yticks([],[])
ax.set_yticks([], minor=True)
plt.title(headerTokens[simd] + " of 2^27*4 bytes as float and double")
plt.rcParams['figure.dpi'] = 360
right_side = ax.spines["right"]
right_side.set_visible(False)
top_side = ax.spines["top"]
top_side.set_visible(False)
plt.savefig(fileSave + "serial-"+ headerTokens[simd] + "-equiv-N"+ str(2**27)+"-float-double")
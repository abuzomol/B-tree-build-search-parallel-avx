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

plt.rcParams.update({'figure.max_open_warning': 0})

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
processors = [2**i for i in range(0, int(math.log(noOfProcessors,2)) + 1)]
print("processors::" , processors)

now = datetime.datetime.now()
print ("Current date and time : ")
print (now.strftime("%Y-%m-%d"))
day = now.strftime("%Y-%m-%d")

programs = ["parallelBuildSearchInt", "parallelBuildSearchLong",
            "parallelBuildSearchFloat", "parallelBuildSearchDouble"]
shortPrograms = {"parallelBuildSearchInt":"int", "parallelBuildSearchLong":"long",
            "parallelBuildSearchFloat":"float", "parallelBuildSearchDouble":"double"}
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

for N in itemSize: #3
    for program in programs: #2
        for processor in processors: #4        
            csvfileName = filePath +program + str(processor) + "-" + str(N) +  ".csv"
            sheets = sheets + [csvfileName]
            figureLabels = figureLabels + [ ["2^"+str(int(math.log(N,2))) , shortPrograms[program], str(processor)] ]

[print(sheet) for sheet in sheets]
[print(label) for label in figureLabels]

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
#*******************************************************
#Plot same number of processors same N same type two builds and 3 different search 
for i in range(len(dfs)):
    fig, ax = plt.subplots()
    #dfs[i]['node size'] = pd.to_numeric(dfs[i]['node size']).astype('int')
    line1, = ax.plot(nodeSizes, dfs[i][cols[0]], label = headerTokens[cols[0]] ) #horizontal build
    line2, = ax.plot(nodeSizes, dfs[i][cols[1]], label = headerTokens[cols[1]]) #vertical build
    # ax.legend(loc='upper right')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True,ncol=4)
    plt.xlabel('nodes sizes')
    ax.xaxis.set_label_coords(1.05, -0.025)
    plt.ylabel('time(s)')
    plt.title("parallel build comparisons N = " + figureLabels[i][0] + " " + figureLabels[i][1] + " P = " +figureLabels[i][2])
    plt.rcParams['figure.dpi'] = 360
    right_side = ax.spines["right"]
    right_side.set_visible(False)
    top_side = ax.spines["top"]
    top_side.set_visible(False)
    print(i, fileSave + "parallel-build-compare-"+ figureLabels[i][0] + "-" + figureLabels[i][1] + "-p" +figureLabels[i][2])
    plt.savefig(fileSave + "parallel-build-compare-"+ figureLabels[i][0] + "-" + figureLabels[i][1] + "-p" +figureLabels[i][2])
    fig, ax = plt.subplots()
    if figureLabels[i][1] in ["int", "float"]:
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
    plt.title("parallel search comparisons N = " + figureLabels[i][0] + " " + figureLabels[i][1] + " P = " +figureLabels[i][2])
    # plt.yticks([],[])
    # ax.set_yticks([], minor=True)
    # y_ticks = np.arange(0, 10, .5)
    # plt.yticks(y_ticks)
    plt.rcParams['figure.dpi'] = 360
    right_side = ax.spines["right"]
    right_side.set_visible(False)
    top_side = ax.spines["top"]
    top_side.set_visible(False)
    print(i, fileSave + "parallel-search-compare-"+ figureLabels[i][0] + "-" + figureLabels[i][1] + "-p" +figureLabels[i][2])
    plt.savefig(fileSave + "parallel-search-compare-"+figureLabels[i][0] + "-" + figureLabels[i][1] + "-p" +figureLabels[i][2])
#*************************************************************
# Plot same P same type different N for int, long, double and float
types=['int','long','float','double']
for i in range(0,len(types)*len(processors)):
    for col in cols:
        fig, ax = plt.subplots()
        if col < 6:
            for j in range(len(itemSize)): 
                t = j*len(types)*len(processors)
                line, = ax.plot(nodeSizes,dfs[i+t][col],label = "N =" + figureLabels[i+t][0])
        else:#SIMD
            for j in range(len(itemSize)): 
                t = j*len(types)*len(processors)
                line, = ax.plot(nodeSizes[1::2], dfs[i+t][col][1::2], label = "N =" + figureLabels[i+t][0])
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
        fancybox=True, shadow=True,ncol=4)
        plt.xlabel('nodes sizes')
        ax.xaxis.set_label_coords(1.05, -0.025)
        plt.ylabel('time(s)')
        plt.title("parallel " + headerTokens[col] + " with different N " + figureLabels[i][1] + " P =" + figureLabels[i][2])
        plt.rcParams['figure.dpi'] = 360
        right_side = ax.spines["right"]
        right_side.set_visible(False)
        top_side = ax.spines["top"]
        top_side.set_visible(False)
        #sns.despine();
        print(i, fileSave + "parallel-" + headerTokens[col] + "-with-different-N-" + figureLabels[i][1] + "-p" + figureLabels[i][2])
        plt.savefig(fileSave + "parallel-" + headerTokens[col] + "-with-different-N-" + figureLabels[i][1] + "-p" + figureLabels[i][2])
#*************************************************************
# Plot same N, same col, same type with different processors
for i in range(len(itemSize)): # 3 N values
    for j in range(len(types)): # 4 types
        for col in cols: # 5 functions
            fig, ax = plt.subplots()
            for processor in range(len(processors)): # 4 processors
                k = i*len(itemSize)*len(processors) + j*len(types) + processor
                print(k, figureLabels[k])
                if col < 6:
                    line, = ax.plot(nodeSizes, dfs[k][col], label = " P = " + str(2**processor))
                else:
                    line, = ax.plot(nodeSizes[1::2], dfs[k][col][1::2], label = " P = " + str(2**processor))
            ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
            fancybox=True, shadow=True,ncol=4)
            plt.xlabel('nodes sizes')
            ax.xaxis.set_label_coords(1.05, -0.025)
            plt.ylabel('time(s)')
            plt.title("parallel " + headerTokens[col] + " N = " + figureLabels[i*len(types)*len(processors)][0] + " " + types[j])
            plt.rcParams['figure.dpi'] = 360
            right_side = ax.spines["right"]
            right_side.set_visible(False)
            top_side = ax.spines["top"]
            top_side.set_visible(False)
            #sns.despine();
            print(i, fileSave + "parallel-" + headerTokens[col] + "-N-" + figureLabels[i*len(types)*len(processors)][0] + "-"+types[j] + "-different-p")
            plt.savefig(fileSave + "parallel-" + headerTokens[col] + "-N-" + figureLabels[i*len(types)*len(processors)][0] + "-"+types[j]+"-different-p")

# #Plot same N same columns different types (no need for parallel, likely same result as serial)
# for i in range(len(itemSize)):
#     for col in cols:
#         fig, ax = plt.subplots()
#         for j in range(4):
#             #dfs[i]['node size'] = pd.to_numeric(dfs[i]['node size']).astype('int')
#             line, = ax.plot(nodeSizes[1::2], dfs[i*4+j][col][1::2], label = types[j])
#         ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
#           fancybox=True, shadow=True,ncol=4)
#         plt.xlabel('nodes sizes')
#         ax.xaxis.set_label_coords(1.05, -0.025)
#         plt.ylabel('time(s)')
#         # plt.yticks([],[])
#         # ax.set_yticks([], minor=True)
#         plt.title(headerTokens[col] + " of 2^" + str(int(math.log(itemSize[i],2))) + " of ints longs floats & doubles" )
#         plt.rcParams['figure.dpi'] = 360
#         right_side = ax.spines["right"]
#         right_side.set_visible(False)
#         top_side = ax.spines["top"]
#         top_side.set_visible(False)
#         plt.savefig(fileSave + "parallel-"+ headerTokens[col] + "-same-N"+ str(itemSize[i]))

# #Plot fair comparisons, int and long, float and double except simd (no need more likely same result as serial)
# for col in [2,3,4,5]:
#     fig, ax = plt.subplots()
#     line1, = ax.plot(nodeSizes, dfs[5][col], label = types[1]) 
#     line2, = ax.plot(nodeSizes, dfs[8][col], label = types[0]) 
#     ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
#           fancybox=True, shadow=True,ncol=4)
#     plt.xlabel('nodes sizes')
#     ax.xaxis.set_label_coords(1.05, -0.025)
#     plt.ylabel('time(s)')
#     # plt.yticks([],[])
#     # ax.set_yticks([], minor=True)
#     plt.title(headerTokens[col] + " of 2^27*4 bytes as int and long")
#     plt.rcParams['figure.dpi'] = 360
#     right_side = ax.spines["right"]
#     right_side.set_visible(False)
#     top_side = ax.spines["top"]
#     top_side.set_visible(False)
#     plt.savefig(fileSave + "parallel-"+ headerTokens[col] + "-equiv-N"+ str(2**27) + "-int-long")
#     fig, ax = plt.subplots()
#     line1, = ax.plot(nodeSizes, dfs[7][col], label = types[3]) 
#     line2, = ax.plot(nodeSizes, dfs[10][col], label = types[2]) 
#     ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
#           fancybox=True, shadow=True,ncol=4)
#     plt.xlabel('nodes sizes')
#     ax.xaxis.set_label_coords(1.05, -0.025)
#     # plt.ylabel('time(s)')
#     # plt.yticks([],[])
#     ax.set_yticks([], minor=True)
#     plt.title(headerTokens[col] + " of 2^27*4 bytes as float and double")
#     plt.rcParams['figure.dpi'] = 360
#     right_side = ax.spines["right"]
#     right_side.set_visible(False)
#     top_side = ax.spines["top"]
#     top_side.set_visible(False)
#     plt.savefig(fileSave + "parallel-"+ headerTokens[col] + "-equiv-N"+ str(2**27)+"-float-double")
# #plot simd operations
# simd = 6
# fig, ax = plt.subplots()
# line1, = ax.plot(nodeSizes[1::2], dfs[5][simd][1::2], label = types[1]) 
# line2, = ax.plot(nodeSizes[1::2], dfs[8][simd][1::2], label = types[0]) 
# ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
#         fancybox=True, shadow=True,ncol=4)
# plt.xlabel('nodes sizes')
# ax.xaxis.set_label_coords(1.05, -0.025)
# plt.ylabel('time(s)')
# # plt.yticks([],[])
# # ax.set_yticks([], minor=True)
# plt.title(headerTokens[simd] + " of 2^27*4 bytes as int and long")
# plt.rcParams['figure.dpi'] = 360
# right_side = ax.spines["right"]
# right_side.set_visible(False)
# top_side = ax.spines["top"]
# top_side.set_visible(False)
# plt.savefig(fileSave + "parallel-"+ headerTokens[simd] + "-equiv-N"+ str(2**27) + "-int-long")
# fig, ax = plt.subplots()
# line1, = ax.plot(nodeSizes[1::2], dfs[7][simd][1::2], label = types[3]) 
# line2, = ax.plot(nodeSizes[1::2], dfs[10][simd][1::2], label = types[2]) 
# ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
#         fancybox=True, shadow=True,ncol=4)
# plt.xlabel('nodes sizes')
# ax.xaxis.set_label_coords(1.05, -0.025)
# # plt.ylabel('time(s)')
# # plt.yticks([],[])
# ax.set_yticks([], minor=True)
# plt.title(headerTokens[simd] + " of 2^27*4 bytes as float and double")
# plt.rcParams['figure.dpi'] = 360
# right_side = ax.spines["right"]
# right_side.set_visible(False)
# top_side = ax.spines["top"]
# top_side.set_visible(False)
# plt.savefig(fileSave + "parallel-"+ headerTokens[simd] + "-equiv-N"+ str(2**27)+"-float-double")
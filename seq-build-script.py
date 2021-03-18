"""
This is a script to run multiple dataContainer and measures the init and access time from chrono library outputs. It then outputs csv files with time as prefix.
"""
import shlex
import subprocess
import datetime
import csv
import matplotlib.pyplot as plt
import sys
import matplotlib
matplotlib.use('Agg')  # Must be before importing matplotlib.pyplot or pylab!

now = datetime.datetime.now()
print("Current date and time : ")
print(now.strftime("%Y-%m-%d"))
day = now.strftime("%Y-%m-%d")

programs = ["seqBuildSearchInt", "seqBuildSearchLong",
            "seqBuildSearchFloat", "seqBuildSearchDouble"]
header = "N,node size,build horizontal(s),build vertical(s),seq search(s),binary search(s), simd search(s)\n"
pwd = subprocess.run('pwd', stdout=subprocess.PIPE,
                     universal_newlines=True).stdout[:-1]
programPath = pwd + '/code/serial/'
filePath = pwd + "/data"
print(filePath)

print(programPath)

# itemSize = [2**10, 2**11,10000]
itemSize = [2**25, 2**26, 2**27]
for program in programs:
    for N in itemSize:
        fileName = filePath + "/"+ program + "-" + str(N) + ".csv"
        with open(fileName, "w") as fileInput:
            fileInput.write(header)
# scan through second layer node size
# nodeSizes = [16,32,48]
nodeSizes = [8*i for i in range(1, 65)]
#L = [17]
for N in itemSize:
    for C in nodeSizes:
        for program in programs:
            print(programPath + program, str(N), str(C))
            process = subprocess.run(
                [programPath + program, str(N), str(C)], stdout=subprocess.PIPE, universal_newlines=True)
            output = process.stdout
            print(output)
            halfSplit = output.split(" ")
            splitted = [str(N), str(C)] + [halfSplit[i] for i in range(len(halfSplit) - 1)]
            words = ""
            for i in range(len(splitted)):
                words = words + splitted[i] + ","
            words = words + "\n"
            fileName = filePath + "/" + program + "-" + str(N) + ".csv"
            with open(fileName, "a") as fileInput:
                fileInput.write(words)

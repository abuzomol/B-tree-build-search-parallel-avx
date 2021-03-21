"""
This is a script to run multiple B-tree build and search files over multiple processors. It then outputs csv files with time as prefix.
"""
import math
import shlex
import subprocess
import datetime
import csv
import matplotlib.pyplot as plt
import sys
import getopt
import matplotlib
matplotlib.use('Agg')  # Must be before importing matplotlib.pyplot or pylab!

try:
    opts, args = getopt.getopt(sys.argv, "hi:o:")
except getopt.GetoptError:
    print("parallel-build-script.py -p <no of processors>")
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print("parallel-build-script.py -p <no of processors>")
        sys.exit()
    elif opt == '-p':
        print(arg)
noOfProcessors = int(sys.argv[2])
print(str(sys.argv), noOfProcessors)
processors = [str(2**i)
              for i in range(0, int(math.log(noOfProcessors, 2)) + 1)]
print(processors)
now = datetime.datetime.now()
print("Current date and time : ")
print(now.strftime("%Y-%m-%d"))
day = now.strftime("%Y-%m-%d")

programs = ["parallelBuildSearchInt", "parallelBuildSearchLong",
            "parallelBuildSearchFloat", "parallelBuildSearchDouble"]

header = "N,node size,build horizontal(s),build vertical(s),seq search(s),binary search(s), simd search(s)\n"

pwd = subprocess.run('pwd', stdout=subprocess.PIPE,
                     universal_newlines=True).stdout[:-1]
programPath = pwd + '/code/parallel/'
filePath = pwd + "/data"
print(filePath)

print(programPath)

# itemSize = [2**10, 2**11, 2**12]
itemSize = [2**25, 2**26, 2**27]
for program in programs:
    for processor in processors:
        for N in itemSize:
            fileName = filePath + "/" + program + \
                processor + "-" + str(N) + ".csv"
            with open(fileName, "w") as fileInput:
                fileInput.write(header)
# scan through second layer node size
# nodeSizes = [16, 32, 48]
nodeSizes = [8*i for i in range(1, 65)]
for N in itemSize:
    for C in nodeSizes:
        for program in programs:
            for processor in processors:
                runProgram = programPath + program+processor
                print(runProgram, str(N), str(C))
                process = subprocess.run([runProgram, str(N), str(C)], stdout=subprocess.PIPE, universal_newlines=True)
                output = process.stdout
                print(output)
                halfSplit = output.split(" ")
                # print(halfSplit)
                splitted = [str(N), str(C)] + [halfSplit[i] for i in range(len(halfSplit) - 1)]
                words = ""
                for i in range(len(splitted)):
                    words = words + splitted[i] + ","
                words = words + "\n"
                fileName = filePath + "/"+program + \
                    processor + "-" + str(N) + ".csv"
                with open(fileName, "a") as fileInput:
                    fileInput.write(words)

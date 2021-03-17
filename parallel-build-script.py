"""
This is a script to run multiple B-tree build and search files over multiple processors. It then outputs csv files with time as prefix.
"""
import sys, getopt
import matplotlib
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt
import csv
import datetime
import subprocess
import shlex
import math

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
noOfProcessors = int(sys.argv[2])
print(str(sys.argv), noOfProcessors)
processors = [str(2**i) for i in range(0, int(math.log(noOfProcessors,2)) + 1)]
print(processors)
now = datetime.datetime.now()
print ("Current date and time : ")
print (now.strftime("%Y-%m-%d"))
day = now.strftime("%Y-%m-%d")

programs = ["parallelPreProcessInt", "parallelPreProcessLong"]

header = "N,node size,build horizontal(s),build vertical(s),seq search(s),Binary search(s)\n"
pwd = subprocess.run('pwd',stdout=subprocess.PIPE, universal_newlines=True).stdout[:-1]
programPath = pwd + '/'
filePath = pwd + "/timePerformance" 
print(filePath)

print(programPath)

itemSize = [2**25, 2**26, 2**27]
for program in programs:
    for processor in processors:
        for N in itemSize:
            fileName = filePath + "/"+ day + "-" +program + processor + "-" + str(N) +  "-time.csv"
            with open(fileName,"w") as fileInput:
                fileInput.write(header)
# scan through second layer node size
nodeSizes = [1,4, 8, 16, 32, 64, 128, 256,512]
#L = [17]
for N in itemSize:
    for C in nodeSizes:
        for program in programs:
            for processor in processors:
                print(programPath + program+processor,str(N),str(C))
                process = subprocess.run([programPath + program+processor,str(N),str(C)],stdout=subprocess.PIPE, universal_newlines=True)
                output = process.stdout
                halfSplit =  output.split(" ")[:5]
                print("output splitted",halfSplit)
                splitted = [str(N), str(C)] +  [halfSplit[0]] +  [halfSplit[1]] + [halfSplit[2]] + [halfSplit[3]] 
                print("words",splitted)
                words = ""
                for i in range(len(splitted)):
                    words = words + splitted[i] + "," 
                words = words + "\n"
                #words = splitted[0] + "," + splitted[1] + "," + splitted[2] + "," + splitted[3] + "\n"
                fileName = filePath + "/"+ day + "-" +program + processor + "-" + str(N) +  "-time.csv"
                with open(fileName,"a") as fileInput:
                    fileInput.write(words)

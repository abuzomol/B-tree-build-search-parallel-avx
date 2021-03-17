"""
This is a script to run multiple dataContainer and measures the init and access time from chrono library outputs. It then outputs csv files with time as prefix.
"""
import sys
import matplotlib
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt
import csv
import datetime
import subprocess
import shlex

now = datetime.datetime.now()
print ("Current date and time : ")
print (now.strftime("%Y-%m-%d"))
day = now.strftime("%Y-%m-%d")

programs = ["seqBuildSearchLong", "seqBuildSearchInt"]
header = "N,node size,build horizontal(s),build vertical(s),seq search(s),Binary search(s)\n"
pwd = subprocess.run('pwd',stdout=subprocess.PIPE, universal_newlines=True).stdout[:-1]
programPath = pwd + '/'
filePath = pwd + "/timePerformance" 
print(filePath)

print(programPath)

itemSize = [2**25, 2**26, 2**27]
for program in programs:
    for N in itemSize:
        fileName = filePath + "/"+ day + "-" +program + "-" + str(N) +  "-time.csv"
        with open(fileName,"w") as fileInput:
            fileInput.write(header)
# scan through second layer node size
nodeSizes = [1,4, 8, 16, 32, 64, 128, 256,512]
#L = [17]
for N in itemSize:
    for C in nodeSizes:
        for program in programs:
            print(programPath + program,str(N),str(C))
            process = subprocess.run([programPath + program,str(N),str(C)],stdout=subprocess.PIPE, universal_newlines=True)
            output = process.stdout
            halfSplit =  output.split(" ")[:5]
            print("output splitted",halfSplit)
            splitted = [str(N), str(C)] + [halfSplit[0]] + [halfSplit[1]] + [halfSplit[2]] + [halfSplit[3]] 
            print("words",splitted)
            words = ""
            for i in range(len(splitted)):
                words = words + splitted[i] + "," 
            words = words + "\n"
            #words = splitted[0] + "," + splitted[1] + "," + splitted[2] + "," + splitted[3] + "\n"
            fileName = filePath + "/"+ day + "-" +program + "-" + str(N) +  "-time.csv"
            with open(fileName,"a") as fileInput:
                fileInput.write(words)

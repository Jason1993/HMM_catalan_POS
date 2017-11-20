from __future__ import division
import time
import os
import sys
start = time.clock()

file1 = open(sys.argv[1],"r")
#Build tag set
tagset = ["ST"]

#Build transition matrix
numCount = {}
emiCount = {}
worddic = {}
for line in file1:
    line = line.strip()
    temp = line.split(" ")
    for i in range(len(temp)):
        if (i == 0):
            if ("ST" in numCount):
                curtag = temp[i][len(temp[i])-2:]
                if (curtag in numCount["ST"]):
                    numCount["ST"][curtag] += 1
                else:
                    numCount["ST"][curtag] = 1
            else:
                numCount["ST"] = {}
                curtag = temp[i][len(temp[i])-2:]
                numCount["ST"][curtag] = 1
        else:
            curtag = temp[i][len(temp[i]) - 2:]
            pretag = temp[i-1][len(temp[i-1]) - 2:]
            if (pretag in numCount):
                if (curtag in numCount[pretag]):
                    numCount[pretag][curtag] += 1
                else:
                    numCount[pretag][curtag] = 1
            else:
                numCount[pretag] = {}
                numCount[pretag][curtag] = 1

        if (curtag not in tagset):
            tagset.append(curtag)
        fooword = temp[i][0:len(temp[i]) - 3]
        if (curtag in emiCount):
            if fooword not in emiCount[curtag]:
                emiCount[curtag][fooword] = 1
            else:
                emiCount[curtag][fooword] += 1
        else:
            emiCount[curtag] = {}
            emiCount[curtag][fooword] = 1
        if (fooword in worddic):
            worddic[fooword][curtag] = 1
        else:
            worddic[fooword] = {}
            worddic[fooword][curtag] = 1
#Smoothing transition matrix
for i in tagset:
    if (i == "EN"):
        continue
    else:
        for j in tagset:
            if (j in numCount[i]):
                numCount[i][j] += 1
            else:
                numCount[i][j] = 1


file1.close()
input_file=open("hmmmodel.txt", "w")
input_file.write(str(tagset)+"\n")
input_file.write(str(numCount))
input_file.write("\n")
input_file.write(str(emiCount))
input_file.write("\n")
input_file.write(str(worddic))
input_file.close()
#print time.clock()-start

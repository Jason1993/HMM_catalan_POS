from __future__ import division
from math import log
import os
import sys
filemodel = open("hmmmodel.txt","r")
fileget = filemodel.read().split("\n")
tagset = eval(fileget[0])
transi = eval(fileget[1])
emissi = eval(fileget[2])
worddic = eval(fileget[3])
#Build Transition probability matrix
tranpro = {}
for i in tagset:
    tranpro[i] = {}
    for j in tagset:
        tranpro[i][j] = 0
for pre in transi:
    counttemp = 0
    for cur in transi[pre]:
        counttemp += int(transi[pre][cur])
    for cur in transi[pre]:
        tranpro[pre][cur] = log(float(int(transi[pre][cur])/counttemp))

#Build Emission probability matrix
emispro = {}
emistotal = 0
for i in tagset:
    emispro[i] = {}
for cur in emissi:
    counttemp = 0
    for item in emissi[cur]:
        counttemp += int(emissi[cur][item])
    emistotal += counttemp
    for item in emissi[cur]:
        emispro[cur][item] = log(float(int(emissi[cur][item])/counttemp))
tagset.remove("ST")
#Decoding progress using Viterbi algorithm
def Viterbi(sentence):
    backPointer = {}
    probMatrix = {}
    sentence = sentence.strip()
    tokens = sentence.split(" ")
    tags = {}
    for i in range(len(tokens)):
        probMatrix[i] = {}
        backPointer[i] = {}
        if (i == 0):
            preTag = "ST"
            if tokens[i] in worddic:
                taglist = worddic[tokens[i]].keys()
            else:
                taglist = tranpro[preTag]
            for traPro in taglist:
                if (tokens[i] in emispro[traPro]):
                    probMatrix[i][traPro] = tranpro[preTag][traPro] + emispro[traPro][tokens[i]]
                else:
                    probMatrix[i][traPro] = tranpro[preTag][traPro] + log(1/emistotal)
                backPointer[i][traPro] = preTag
        else:
            if tokens[i] in worddic:
                taglist = worddic[tokens[i]].keys()
            else:
                taglist = tranpro.keys()
                taglist.remove("ST")
            for curTag in taglist:
                maxVal = -100000
                for preTag in probMatrix[i-1]:
                    if (preTag == "ST"):
                        continue
                    curTransi = tranpro[preTag][curTag] + probMatrix[i-1][preTag]
                    if (curTransi > maxVal):
                        maxVal = curTransi
                        backPointer[i][curTag] = preTag
                    if (tokens[i] in emispro[curTag]):
                        probMatrix[i][curTag] = curTransi + emispro[curTag][tokens[i]]
                    else:
                        probMatrix[i][curTag] = curTransi + log(1/emistotal)
    maxFin = -100000
    for it in probMatrix[len(tokens)-1]:
        if (probMatrix[len(tokens)-1][it] > maxFin):
            maxFin = probMatrix[len(tokens)-1][it]
            tags[len(tokens)-1] = it

    for i in range(len(tokens)-2,-1,-1):
        tags[i] = backPointer[i+1][tags[i+1]]

    res =""
    for i in range(len(tokens)):
        if (i < len(tokens)-1):
            res += tokens[i]+"/"+tags[i]+" "
        else:
            res += tokens[i]+"/"+tags[i]+"\n"
    return res

file2 = open(sys.argv[1],"r")
output_file=open("hmmoutput.txt", "w")
for line in file2:
    line.strip()
    res = Viterbi(line)
    output_file.write(res)
file2.close()
output_file.close()
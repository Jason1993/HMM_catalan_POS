from __future__ import division
ansfile = open("catalan_corpus_dev_tagged.txt","r")
resfile = open("hmmoutput.txt","r")
ans = ansfile.read().split("\n")
res = resfile.read().split("\n")
rightcount = 0
wrongcount = 0
for i in range(len(ans)):
    ansline = ans[i]
    resline = res[i]
    anstemp = ansline.split(" ")
    restemp = resline.split(" ")
    for j in range(len(anstemp)):
        atag = anstemp[j][len(anstemp[j])-2:]
        rtag = restemp[j][len(restemp[j])-2:]
        if (atag == rtag):
            rightcount += 1
        else:
            wrongcount += 1

print rightcount/(wrongcount+rightcount)
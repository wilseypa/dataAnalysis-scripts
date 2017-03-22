from ReadResults import *
import os
import subprocess
import stats
import time
import sys
from utils import *
from Project import *
from RPTestSeq import runLabeler
from RecursLSH import *

'''************** AUTHOR NICK *************'''

def runRecursLSH(argsdict, data, inlbl, fPath, fName, fileN,bits):
    start = time.time()
    k = int(argsdict['clusters'][0])
    projector = Project(len(data[0]),bits,projtype='dbf')
    clusterer = RecLSH(projector=projector)
    estcents = clusterer.findDensityModes(data,k,bits)
    end = time.time()
    clusterer.findNN(data,data[0],int(argsdict['clusters'][0]),bits)
    
    return estcents, (end-start), sys.getsizeof(clusterer)

def runRecursLSHSize(argsdict, data, inlbl, fPath, fName, fileN,bits):
    start = time.time()
    projector = Project(len(data[0]),bits,projtype='dbf')
    clusterer = RecLSH(projector=projector)
    estcents = clusterer.findDensityModes(data,int(argsdict['clusters'][0]),bits).values()
    end = time.time()
    clusterer.findNN(data,data[0],int(argsdict['clusters'][0]),bits)
    
    return sys.getsizeof(clusterer),(end-start)
    

def runLSHSeq(argsdict, fPath, fileN, fName, i, outFN, runTag, foName, GenTime, bits):
    data = readInputFromFile(fileN + "_RAW",'float')
    inlbl = readInputFromFile(fileN + "_LBLONLY.csv",'int')
    
    
    if(argsdict["exec"][0] == "size"):
        size, time = runRecursLSHSize(argsdict, data, inlbl, fPath, fName, fileN, bits)
        
        outfile = file(outFN, 'a')
        outfile.write('pyRecursLSH' +  ',' + str(argsdict[argsdict['param'][0]][0]) + ',' + foName + str(i) + ',' + str(0) + ',' + str(time) + ',' + str(0)
                  +  ',' + str(0) + ',' + str(0) + ',' + str(0) + ',' + str(0)  
                  + ',' + str(0) + ',' + str(0) + ',' + str(0) + ',' + str(time) + ',' + str(size) + '\n')
        outfile.close()
        
    else:
        cents, rtime, runSize = runRecursLSH(argsdict, data, inlbl, fPath, fName, fileN, bits)
                
        
        outfile = file(fileN + 'RecursCENTS','w')
        #Output Labeled
        outfile.write(str(len(cents))+'\n'+str(len(cents[0]))+'\n')
        for l in xrange(len(cents)):
            for dim in xrange(len(cents[0])):
                outfile.write(str(cents[l][dim]) +'\n')
        outfile.close()
        
        rc = runLabeler("",fileN+"RecursCENTS",fileN+"_RAW")
        
        if(rc == 0 or argsdict['exec'][0] == "size"):
            inP = fileN+"RecursCENTS.labeled"
            lblN = fileN + '_LBLONLY.csv'
            sigCol = fileN + '_SIG.csv'
            
            ari,nmi,ami,homogeneity,completeness,vscore,fmi,aTime,tt = runAnalysis(argsdict, lblN, inP, outFN, sigCol, 1)
            
            print "\tRecursLSHSeq_" + str(bits) + ": " + str([ari,nmi,ami,homogeneity,completeness,vscore,fmi,aTime])
            
            outfile = file(outFN, 'a')
            outfile.write('pyRecursiveLSH_' + str(bits) + 'b,'  + str(argsdict[argsdict['param'][0]][0]) + ',' + foName + str(i) + ',' + str(GenTime) + ',' + str(rtime) + ',' + str(aTime)
                          + ',' + str(ari) + ',' + str(nmi) + ',' + str(ami) + ',' + str(homogeneity)  
                          + ',' + str(completeness) + ',' + str(vscore) + ',' + str(fmi) + ',' + str(rtime) + ',' + str(runSize) + '\n')
            outfile.close()
        else:
            print str(i) + ": Labeler Returned 1, skipping analysis"
        
        
    return

def runRecursLSHSeq(argsdict, fPath, fileN, fName, i, outFN, runTag, foName, GenTime):
    bits = [7, 15, 31, 63]
    
    for b in range(0, 3):
        runLSHSeq(argsdict,fPath,fileN,fName,i,outFN,runTag,foName,GenTime,bits[b]);
        
    return
        

'''****************************************'''
'''****************************************'''

##    python MultiRun.py 1-22-17
##    python MultiRun.py [OutputFolderName] [option=value]
##    python MultiRun.py 1-22-17 vectors=100 clusters=6 multirun=5 batches=5

'''*************** OPTIONS ****************

    **General Options**
        -exec (default all)    -Determine what algorithms to run against generated dataset
                                'all' - use RPHash, sklearn, and LSHKit (see req's in readme)
                                'rphash' 
                                'lshkit' 
                                'cluster': rphash + sklearn
                                'LSH': rphash + lshkit
                                'none'
    
        -scaling (default true)     -Toggle scaling of generated data
        -minValue (default -.999)    -Max value of output data
        -maxValue (default .999)    -Min value of output data
        
        -dim (default 100)        -Number of significant columns to generate
        -dummyCols (default 50) -Number of uncorrelated columns to generate
        
        -clusters (default 3)    -Number of clusters to generate
        -vectors (default 5)    -Number of vectors to generate

        -charts (default pdf)     -Generated chart format (save, show, none, all, png, pdf)
    ____________________________________

    **Generation Distribution Options**
        -dist (default gauss)    -Distribution to generate points on
            -gauss or normal        -Generate points on gaussian distribution
            -uniform or uni         -Generate points uniformly
            -binomial or binom      -Generate points using a binomial distribution
            -exponential or exp     -Generate points using an exponential distribution
    ____________________________________
   
    **CENTROID OPTIONS**
        -corg (default random)     -Organization of clusters to be generated (pairs, triplets, etc.)
                                    -random, bi, tri, quad, all
        -cdist (default .4)     -Target distance of cluster centroid orgs
        -csigma (default .1)    -Deviation of a cluster
        -ccounts (default random) -Cluster counts to partition total vectors into
                                    -random, equal, (TODO)separated
    ____________________________________

    **Output Randomization Options**
        -rshuf (default true)  (true, false) -Randomize the vectors (Rows)
        -cshuf (default random) (separated, intermixed, random)
                                    -Determine how to shuffle the columns; separated keeps significant
                                        columns stacked on low indexed features and dummy columns on 
                                        high indexed features; intermixed disperses evenly; random
                                        performs a shuffle on the columns
        -noise (default 0%) (0-1)  -TODO Amount of noise to add to final output
    ____________________________________

```****************************************'''

from DataGenerator import *
from RPTestSeq import *
from LSHKitSeq import *
from ScikitSeqs import *
from utils import *
from RecursLSHTestSeq import *
import sys
import os
import datetime
import numpy as np
import subprocess
import time

'''************** AUTHOR NICK *************'''


'''
    MultiRun creates folder directories and output data for multiple runs
        Use the 'exec' argument to control the specific algorithms that are executed
        Each algorithm is run once on the same data set to get a perspective
            of how each performs
'''
def runMultiRun(argsdict, foName, fName, runTag):
    #Check if runtype = rphash/lshkit/all/none
    runs = int(argsdict['batches'][0])
    reps = int(argsdict['multirun'][0])    
    
    #Check for necessary files of each
    if(argsdict["exec"][0] == "all" or argsdict["exec"][0] == "rphash"):
        if not checkRPFiles():
            return
    
    #Create a folder for the current test
    if not os.path.exists('./' + foName + '/'):
        os.mkdir('./' + foName + '/')
        
    #Create our results file and write a header
    outFN = './' + foName + '/Results_' + fName + '_' + str(datetime.date.today()).replace(' ','_') + '.csv'
    
    outfile = file(outFN, 'w')
    outfile.write('Run,' + str(argsdict["param"][0]) + ',fileN,GenTime,ClusteringTime,AnalysisTime,ARI,NMI,AMI,Homogeneity,Completeness,Vscore,FMI,Time,MemKB,WCSSE\n')
    outfile.close()
    
    #For Runs...
    for i in xrange(runs):       
        print str(i) + ": Starting run"
        
        # 1) Generate files for RPHash, LSHkit
        GenTime = runGenerator(foName, fName + str(i), argsdict)
        fPath = './' + foName + '/' + fName + str(i) + '/'
        fileN = fPath + fName + str(i)
        
        for r in xrange(reps):
        
            if(argsdict["exec"][0] == "all" or argsdict["exec"][0] == "lshkit"):
                # Run LSHKIT
                runLSHKit(fPath, fileN)
            
            if(argsdict["exec"][0] == "all" or argsdict["exec"][0] == "sklearn" or argsdict["exec"][0] == "cluster"):
                runSciKitSeq(argsdict, fPath, fileN, fName, i, outFN, runTag, foName, GenTime)
            
            if(argsdict["exec"][0] == "size"):
                runSizeAnalysis(argsdict, fPath, fileN, fName, i, outFN, runTag, foName, GenTime)
                
            if(argsdict["exec"][0] == "all" or argsdict["exec"][0] == "pylsh" or argsdict["exec"][0] == "cluster" or argsdict["exec"][0] == "size"):
                runRecursLSHSeq(argsdict, fPath, fileN, fName, i, outFN, runTag, foName, GenTime) 
            
            if(argsdict["exec"][0] == "all" or argsdict["exec"][0] == "rphash" or argsdict["exec"][0] == "cluster" or argsdict["exec"][0] == "size"):
                # Run RPHash
                runRPSeq(argsdict, fPath, fileN + '_RAW', fName, i, outFN, runTag,foName,GenTime)
            
        
    return
    

'''****************************************'''



'''****************************************'''

'''
Main
    -Read in the args dictionary - this gets passed to the generator
    -Create folders and filenames and run MultiRun
'''
if __name__ == "__main__":
    
    argsdict = {}
    if len(sys.argv) > 1:
        print os.getcwd()
    
        foName = sys.argv[1]
        cRaw = ''
        for i in range(0, len(sys.argv)):
            cRaw += sys.argv[i] + ' '
            
        for farg in sys.argv[2:]:
            (arg,val) = farg.split("=")
        
            argsdict[arg] = [val]
            
        argsdict = argsDefault(argsdict)
        
        runMultiRun(argsdict, foName, foName,'')
        
    else:
        print "Requires [numRuns] [outFolder] [Option=<...>]\n\tSee MultiRun.py for options and information"

'''****************************************'''

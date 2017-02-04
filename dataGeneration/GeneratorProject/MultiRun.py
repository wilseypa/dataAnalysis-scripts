'''****************************************'''

##    python MultiRun.py 5 1-22-17
##    python MultiRun.py [Num of Runs] [OutputFolderName] [option=value]
##    python MultiRun.py 5 1-22-17 vectors=100 clusters=6

'''*************** OPTIONS ****************

    **General Options**
        -exec (default all)    -Determine what programs to use for analysis
                                'all' - use RPHash and LSHKit (see req's)
                                    'rphash', 'lshkit', 'none')
    
        -infile (default null)    -File for input data generation
    
        -scaling (default true)     -Toggle scaling of generated data
        -minValue (default -.999)    -Max value of output data
        -maxValue (default .999)    -Min value of output data
        
        -dim (default 100)        -Number of significant columns to generate
        -dummyCols (default 50) -Number of uncorrelated columns to generate
        
        -clusters (default 3)    -Number of clusters to generate
        -vectors (default 1000)    -Number of vectors to generate

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
from utils import *
import sys
import os
import datetime
import numpy as np
import subprocess
import time

'''
Notes:
    -Data generator for testing algorithms
        -Specifically focused on the LSH algorithms
            -Comparative analysis of old LSH v. new LSH
            -Significance of LSH operation on the data sets
    -Based off of 'generate-from-labelled-dataset.py'

    -Generates data column by column
        -Significant columns are generated using centroids
        -Nonsignificant columns are uniformly distributed

    -Outputs generated data to folder
        -Raw data (no labels)
        -Labeled data
        -Graph Output (Pdf/Png)
        -Configuration output

'''

'''************** AUTHOR NICK *************'''

def runMultiRun(argsdict, foName, fName, runs, runTag):
    #Check if runtype = rphash/lshkit/all/none
    
    
    #Check for necessary files of each
    if not os.path.exists('./RPHash.jar'):
        print "Missing RPHash.jar from root directory - copy before running generator"
        return
    if not os.path.exists('./LabelData.jar'):
        print "Missing LabelData.jar from root directory - copy before running generator"
        return
    
    #Create a folder for the current test
    if not os.path.exists('./' + foName + '/'):
        os.mkdir('./' + foName + '/')
        
    #Create our results file and write a header
    outFN = './' + foName + '/Results_' + fName + '_' + str(datetime.date.today()).replace(' ','_') + '.csv'
    
    outfile = file(outFN, 'w')
    outfile.write('Run,fileN,GenTime,RPTime,AnalysisTime,Purity,Time,MemKB,WCSSE\n')
    outfile.close()
    
    
    #For Runs...
    for i in xrange(runs):       
        print str(i) + ": Starting run"
        
        # 1) Generate files for RPHash, LSHkit
        GenTime = runGenerator(foName, fName + str(i), argsdict)
        
        fPath = './' + foName + '/' + fName + str(i) + '/'
        fileN = fPath + fName + str(i)
               
        if(argsdict["exec"][0] == "all" or argsdict["exec"][0] == "lshkit"):
            # Run LSHKIT
            runLSHKit(fPath, fileN)
        fileN += '_RAW'
        
        
        if(argsdict["exec"][0] == "all" or argsdict["exec"][0] == "rphash"):
            # Run RPHash
            runRPSeq(argsdict, fPath, fileN, fName, i, outFN, runTag,foName,GenTime)
        
    return
    

'''****************************************'''



'''****************************************'''


'''
Main
    -Check if an input file exists
        -if so, use input file to generate the output data
        -if not, use internal method to generate the output data
'''
if __name__ == "__main__":
    
    argsdict = {}
    if len(sys.argv) > 2:
        runs = int(sys.argv[1])
        print os.getcwd()
        print "Starting Batch Generation and Analysis for " + str(runs) + " runs"
    
        foName = sys.argv[2]
        cRaw = ''
        for i in range(0, len(sys.argv)):
            cRaw += sys.argv[i] + ' '
            
        for farg in sys.argv[3:]:
            (arg,val) = farg.split("=")
        
            argsdict[arg] = [val]
            
        argsdict = argsDefault(argsdict)
        
        runMultiRun(argsdict, foName, foName, runs,'')
        
    else:
        print "Requires [numRuns] [outFolder] [Option=<...>]\n\tSee MultiRun.py for options and information"

'''****************************************'''

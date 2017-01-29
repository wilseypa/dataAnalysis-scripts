'''****************************************'''

##    python MultiRun.py 5 1-22-17
##    python MultiRun.py [Num of Runs] [OutputFolderName] [option=value]
##    python MultiRun.py 5 1-22-17 vectors=100 clusters=6

'''*************** OPTIONS ****************

    **General Options**
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
from ReadResults import *
from RPTestSeq import *
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

def runLabeler(fPath, fName, dataN):
    returnCode = subprocess.call("java -jar ./LabelData.jar " + fName+" " + dataN + " " + fName+".labeled" )
    return returnCode

def runReadResults():
    purity = runAnalysis()
    return purity

def runMultiRun(argsdict, foName, fName, runs):
    sysStart = time.time()
    if not os.path.exists('./' + foName + '/'):
        os.mkdir('./' + foName + '/')
    outFN = './' + foName + '/Results_' + fName + '_' + str(datetime.date.today()).replace(' ','_') + '.csv'
    outfile = file(outFN, 'w')
    outfile.write('Run,fileN,GenTime,RPTime,AnalysisTime,Purity\n')
    outfile.close()
    
    for i in xrange(runs):       
        print str(i) + ": Starting run"
        
        # 1) Generate files for RPHash, LSHkit
        GenTime = runGenerator(foName, fName + str(i), argsdict)
        
        fPath = './' + foName + '/' + fName + str(i) + '/'
        fileN = fPath + fName + str(i) + '_RAW'

        # 2) Run RPHash on generated data
        rc, RPTime = runRPjava(int(argsdict['clusters'][0]),fPath ,fileN)

        if(rc == 0): 
            dataN = fileN
            fileN = fileN + 'RPOut.RPHashMultiProj'
            
            # 3) Run labeler on RPHash Centroids
            rc = runLabeler(fPath, fileN, dataN)
            
            if(rc == 0):
                inP = fileN+".labeled"
                lblN = fPath + fName + str(i) + '_LBLONLY.csv'
                sigCol = fPath + fName + str(i) + '_SIG.csv'
                
                purity, aTime = runAnalysis(lblN, inP, fileN + '.Results', sigCol)
                
                outfile = file(outFN, 'a')
                outfile.write(str(i) + ',' + foName + str(i) + ',' + str(GenTime) + ',' + str(RPTime) + ',' + str(aTime) + ',' + str(purity) + '\n')
                outfile.close()
            else:
                print str(i) + ": Labeler Returned 1, skipping analysis"
        else:
            print str(i) + ": RPHash Returned 1, skipping labeler, analysis"
    sysEnd = time.time()    
    print "Finished! Took " + str(sysEnd-sysStart) + " seconds! OR " + str((sysEnd-sysStart)/float(60.0)) + " minutes!"
    print "\tAverage time per run: " + str((sysEnd-sysStart)/runs) + " seconds"
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
        
        runMultiRun(argsdict, foName, foName, runs)
        
    else:
        print "Requires [numRuns] [outFolder] [Option=<...>]\n\tSee MultiRun.py for options and information"
    
    

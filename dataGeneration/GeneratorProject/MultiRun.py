'''****************************************'''

##    python MultiRun.py 5 1-22-17
##    python MultiRun.py [Num of Runs] [OutputFolderName] [option=value]
##    python MultiRun.py 5 1-22-17 vectors=100 clusters=6

'''*************** OPTIONS ****************

    **General Options**
        -infile (default null)    -File for input data generation
    
        -minValue (default -1)    -Max value of output data
        -maxValue (default 1)    -Min value of output data
        
        -dim (default 6)        -Number of significant columns to generate
        -dummyCols (default 50) -Number of uncorrelated columns to generate
        
        -clusters (default 3)    -Number of clusters to generate
        -vectors (default 100)    -Number of vectors to generate

        -charts (default all)     -Generated chart format (save, show, none, all)
    ____________________________________

    **Generation Distribution Options**
        -dist (default uniform)    -Distribution to generate points on
            -gauss or normal        -Generate points on gaussian distribution
            -uniform or uni         -Generate points uniformly
            -binomial or binom
            -exponential or exp
    ____________________________________
   
    **CENTROID OPTIONS**
        -corg (default random)     -Closeness of clusters to be generated
            -random, bi, tri, quad, all
        -cdist (default .4)     -Target distance of cluster centroid orgs
        -csigma (default .1)    -Deviation of a cluster
    ____________________________________

    **Output Randomization Options**
        -shuffle (default all)  (all, cols, rows, none)
    ____________________________________

```****************************************'''

import sys
import os
import datetime
import numpy as np
from DataGenerator import *
import subprocess
from ReadResults import *
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

def runRPjava(numClusters, fPath, fName):
    returnCode = subprocess.call("java -jar ./RPHash.jar " + fName + " " + str(numClusters) + " " + fName + "RPOut multiproj parallel=true offlineclusterer=kmeans runs=5")
    #copy metrics file from root to the current fPath
    return returnCode

def runLabeler(fPath, fName, dataN):
    returnCode = subprocess.call("java -jar ./LabelData.jar " + fName+" " + dataN + " " + fName+".labeled" )
    
    return returnCode

def runReadResults():
    purity = runAnalysis()
    return purity

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
        sysStart = time.time()
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
        if not os.path.exists('./' + foName + '/'):
            os.mkdir('./' + foName + '/')
        outFN = './' + foName + '/Results_' + foName + '_' + str(datetime.date.today()).replace(' ','_') + '.csv'
        outfile = file(outFN, 'w')
        outfile.write('Run,fileN,GenTime,RPTime,AnalysisTime,Purity\n')
        outfile.close()
        for i in xrange(runs):       
            print str(i) + ": Starting run"
            start = time.time()
            runGenerator(foName, foName + str(i), argsdict)
            end = time.time()
            GenTime = (end-start)
            
            fPath = './' + foName + '/' + foName + str(i) + '/'
            fileN = fPath + foName + str(i) + '_RAW'
            start = time.time()
            rc = runRPjava(6,fPath ,fileN)
            end = time.time()
            RPTime = (end-start)
            if(rc == 0): 
                dataN=fileN
                fileN = fileN + 'RPOut.RPHashMultiProj'
                rc = runLabeler(fPath, fileN, dataN)
                
                if(rc == 0):
                    inP = fileN+".labeled"
                    lblN = fPath + foName + str(i) + '_LBLONLY.csv'
                    sigCol = fPath + foName + str(i) + '_SIG.csv'
                    start = time.time()
                    purity = runAnalysis(lblN, inP, fileN + '.Results', sigCol)
                    end = time.time()
                    aTime = (end-start)
                
                
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
    else:
        print "Requires [numRuns] [outFolder] [Option=<...>]\n\tSee MultiRun.py for options and information"
    
    

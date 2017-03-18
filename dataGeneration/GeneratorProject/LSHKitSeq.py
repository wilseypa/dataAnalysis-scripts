import os
import subprocess
import time


'''************** AUTHOR NICK *************'''


'''
    LSHKIT txt2bin
         * \file txt2bin.cpp
         * \brief Convert a dataset file from text to binary.
         *
         * Usage: txt2bin <input> <output>
         *
         * Example input file:
     
             1 0 1 2
             2 3 4 5
             0.5 0.4 0.6 0.1
       
         *
         * Each row of the text file must contain the same number of columns.  Columns are
         * separated by single spaces or tabs.
         *
         *

'''
def runtxt2bin(fName):
    start = time.time()
    returnCode = subprocess.call("./LSHKitBin/txt2bin " + fName + " " + fName + "_LSHKITbin" ,shell=True)
    
    end = time.time()
    return returnCode, (end - start)

'''
    LSHKIT scan
        This program searches for K-NNs by linear scan and generate a benchmark file.
             * \file scan.cpp
             * \brief Linear scan dataset and construct benchmark.
             *
             * This program randomly picks Q points from a dataset as queries, and
             * then linear-scan the database to find K-NN/R-NN for each query to produce
             * a benchmark file.  For each query, the query point itself is excluded
             * from the K-NN/R-NN list.
             *
             * You can specify both K and R and the program will search for the K
             * points closest to queries which are within distance range of R.
             * If K = 0, then all points within distance range of R are returned.
             * The default value of R is the maximal value of float.
             *
            Allowed options:
              -h [ --help ]          produce help message.
              -Q [ -- ] arg (=1)     number of queries to sample.
              -K [ -- ] arg (=1)     number of nearest neighbors.
              --metric arg (=2)      1: L1; 2: L2
              -D [ --data ] arg      dataset path
              -B [ --benchmark ] arg output benchmark file path
'''
def runScan(fName,outFiles):
    start = time.time()
    returnCode = subprocess.call("./LSHKitBin/scan -D " + fName + "_LSHKITbin -B " + fName + "_bench > "+ outFiles +"scanOutput",shell=True)
    
    end = time.time()
    return returnCode, (end - start), fName+"_bench"


'''
    LSHKIT fitdata
         *  \file fitdata.cpp
         *  \brief Gather statistics from dataset for MPLSH tuning.
         *
         *  This program gahters statistical data from a small sample dataset
         *  for automatic MPLSH parameter tuning.  It carries out the following
         *  steps:
         *  -# Sample N points from the dataset. Only those N points will be used for future computation.
         *  -# Sample P pairs of points from the sample, calculate the distance for each pair.
         *  -# Sample Q points from the sample as queries points.
         *  -# Divide the sample into F folds.
         *  -# For i = 1 to F, take i folds and run K-NN search, so the query points
         *     will be searched against sample datasets of N/F, 2N/F, ..., N/F points.
         *
         *  The statistical data is printed to standard output after the progress display.
         *
        Allowed options:
          -h [ --help ]          produce help message.
          -N [ -- ] arg (=0)     number of points to use
          -P [ -- ] arg (=50000) number of pairs to sample
          -Q [ -- ] arg (=1000)  number of queries to sample
          -K [ -- ] arg (=100)   search for K nearest neighbors
          -F [ -- ] arg (=10)    divide the sample to F folds
          -D [ --data ] arg      data file
'''
def runFitData(fName):
    start = time.time()
    returnCode = subprocess.call("./LSHKitBin/fitdata -D " + fName + "LSHKITbin -B "+ fName + "LSHKITbin" ,shell=True)
    
    end = time.time()
    return returnCode, (end - start)

def runMplsh(fName,bench, outFiles):
    start = time.time()
    print fName
    print bench
    print outFiles
    returnCode = subprocess.call("./LSHKitBin/mplsh-run -D " + fName + "LSHKITbin -B " + bench + " > " + outFiles + "/mplshRun", shell=True)
    end = time.time()
    
    return returnCode, (end - start)

def runApost(fName, bench, outFiles):
    start = time.time()
    returnCode = subprocess.call("./LSHKitBin/apost-run -D " + fName + "LSHKITbin -B " + bench + " > " + outFiles + "/apostRun", shell=True)
    end = time.time()
    
    return returnCode, (end - start)

def runForest(fName, bench, outFiles):
    start = time.time()
    returnCode = subprocess.call("./LSHKitBin/forest-run -D " + fName + "LSHKITbin -B " + bench + " > " + outFiles + "/forestRun", shell=True)
    end = time.time()
    
    return returnCode, (end - start)

def runSpectral(fName, bench, outFiles):
    start = time.time()
    returnCode = subprocess.call("./LSHKitBin/run-spectral -D " + fName + "LSHKITbin -B " + bench + " > " + outFiles + "/spectralRun", shell=True)
    end = time.time()
    
    return returnCode, (end - start)

def runLSH(fName, bench, outFiles):
    start = time.time()
    returnCode = subprocess.call("./LSHKitBin/lsh-run -D " + fName + "LSHKITbin -B " + bench + " > " + outFiles + "/lshRun", shell=True)
    end = time.time()
    
    return returnCode, (end - start)


def runLSHKit(fPath, fName):
    start = time.time()
    
    if not os.path.exists(fPath + "LSHKITRes"):
        os.mkdir(fPath + "LSHKITRes")
    
    outFiles = fPath+"LSHKITRes/"
    fName = fName + "_LSHKIT"
    print fName
    returnCode, timest = runtxt2bin(fName)
    
    returnCode, timest, bench = runScan(fName,outFiles)
    
    returnCode,timest = runMplsh(fName, bench, outFiles)
    returnCode,timest = runApost(fName, bench, outFiles)
    returnCode,timest = runForest(fName, bench, outFiles)
    
    returnCode,timest = runSpectral(fName, bench, outFiles)
    returnCode,timest = runLSH(fName, bench, outFiles)
    
    
    #TODO: Aggregate Results into one file
    
    return returnCode, timest


def readLSHKitOut(fPath):
    if os.path.isfile(fPath + 'metrics_time_memkb_wcsse.csv'):
        outfile = file(fPath + 'metrics_time_memkb_wcsse.csv', 'r')
        out = outfile.read();
        outfile.close()
    return out.rstrip()
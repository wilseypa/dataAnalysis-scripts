'''****************************************'''

##    python DataGenerator.py testOutput
##    python DataGenerator.py testOutput [option=value]
##    python DataGenerator.py testOutput infile=inputFile.txt vectors=100

'''*************** OPTIONS ****************

    **General Options**    
        -scaling (default true)     -Toggle scaling of generated data
        -minValue (default -.999)   -Max value of output data
        -maxValue (default .999)    -Min value of output data
        
        -clusters (default 3)     -Number of clusters to generate
        -vectors (default 1000)   -Number of vectors to generate
        -dim (default 100)        -Number of significant columns to generate

        -charts (default pdf)        -Generated chart format (save, show, none, all, png, pdf)
        -output (default all)        -Output 'all' or 'minimal' files (generator)
    ____________________________________
    
    **Noise Options**
        -noise (default 0%) (0-1)      -Amount of noise to add to final output
        -featnoise (default 0%) (0-1)   -Percentage of uncorrelated features to generate
        -vectnoise (default 0%) (0-1)  -Percentage of uncorrelated vectors to generate
    ___________________________________
    
    **Generation Distribution Options**
        -dist (default gauss)	-Distribution to generate points on
            -gauss or normal        -Generate points on gaussian distribution
            -uniform or uni         -Generate points uniformly
	        -binomial or binom      -Generate points using a binomial distribution
            -exponential or exp     -Generate points using an exponential distribution
    ____________________________________
   
    **CENTROID OPTIONS**
	    -corg (default random) 	-Organization of clusters to be generated (pairs, triplets, etc.)
		                            -random, bi, tri, quad, all
	    -cdist (default .4) 	-Target distance of cluster centroid orgs
        -csigma (default .1)	-Deviation of a cluster
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
    ____________________________________   
    
    **Cluster Evolution Options** (IN PROGRESS)
        -evolve (default false) (true, false) -Turn on cluster evolution
        -evint (default 250) -interval to change clusters on
        -evtype (default random) -evolution type (random, *shift - *NOT IMPLEMENTED
    ____________________________________

```****************************************'''

import sys
from DataPlotting import *
from LeeGenerator import *
from PointGenerator import *
from utils import *
from math import floor
import time
import os
import numpy as np

'''
Notes:
	-Data generator for testing algorithms
		-Specifically focused on the LSH algorithms
			-Comparative analysis of old LSH v. new LSH
			-Significance of LSH operation on the data sets
	-Based off of 'generate-from-labelled-dataset.py'

	-Generates data column by column
		-Significant columns are generated using centroids as mean
		-Nonsignificant columns are uniformly distributed

	-Outputs generated data to folder
		-Raw data (no labels)
		-Labeled data
		-Graph Output (pdf/png)
		-Configuration output

'''

'''************** AUTHOR NICK *************'''

'''
    Run data generation with the functions in genRawData (PointGenerator.py)
'''
def generateData(argsDict):

    #Generate the data, centroids, and ids
    data, ids, cents = genRawData(argsDict)
    clearPlots()
    
    if(len(data[0]) >= 2):
        simplePlot((x[0] for x in data), (x[1] for x in data),ids,cents,{});
    if(len(data[0]) >= 3):
        r3DPlot((x[0] for x in data), (x[1] for x in data),(x[2] for x in data), ids,222,cents,{});
    if(len(data[0]) >= 6):
        r3DPlot((x[3] for x in data), (x[4] for x in data),(x[5] for x in data), ids,224,cents,{});
    eucPlot(data, ids,cents,{})
    
    sigCols = data
    data = genDummyCols(argsDict,data)
    
    return data, ids, cents, sigCols

'''
    Output the generated files - RAW, SIG, CENTS, LBL, LBLONLY
'''
def outputFiles(argsDict, fPathRaw, z, ids, cents, sigCols, cRaw):
    
    vectors = int(argsDict["vectors"][0])
    dimensions = int(argsDict["dim"][0])
    featnoise = float(argsDict['featnoise'][0])
    dimensions = int(dimensions - floor(dimensions * featnoise))
    if(dimensions == 0): 
        dimensions = 1;
    charts = argsDict['charts'][0]
    rshuf = argsDict['rshuf'][0]
    output = argsDict['output'][0]
    
    p = int(argsDict["dim"][0])
    
    idsout = []
    
    if rshuf == 'true':
        z, ids, idsout, sigCols = shuffleRows(z, ids, sigCols)

    if(output == 'all' or output == 'minimal'):
        #Output Raw
        outfile = file(fPathRaw + '_RAW','w')
        outfile.write(str(len(z))+'\n'+str(p)+'\n')
        for i in xrange(len(z)):
            for dim in xrange(p):
                outfile.write(str(z[i,dim]))
                if i != len(z)-1 or dim!=p-1:
                    outfile.write('\n')
        outfile.close()
        
        outfile = file(fPathRaw + '_LBLONLY.csv','w')
        outfile.write(str(len(ids))+'\n1\n')
        for i in xrange(len(ids)):
            outfile.write(str(ids[i,0]) + "\n")
        outfile.close()

    if(output == 'all'):
        #output significant columns
        outfile = file(fPathRaw + '_SIG.csv','w')
        for i in xrange(len(sigCols)):
            for dim in xrange(dimensions):
                outfile.write(str(sigCols[i,dim]))
                if(dim != dimensions -1):
                    outfile.write(',')
            if i != len(sigCols):
                outfile.write('\n')
        outfile.close()
            
        #output LSHKIT
        outfile = file(fPathRaw + '_LSHKIT','w')
        for i in xrange(len(z)):
            for dim in xrange(dimensions):
                outfile.write(str(z[i,dim]) + ' ')
            outfile.write('\n')
        outfile.close()
            
        #output centroids
        outfile = file(fPathRaw + '_CENTS.csv','w')
	out = ""
        for i in xrange(len(cents)):
            if(dimensions == 1):
                out += str(cents[i]) + '\n'
            else:
                for dim in xrange(dimensions):
                    out += str(cents[i,dim]) + ','
		out = out[:-1] + '\n'
	outfile.write(out)
        outfile.close()
        
        outfile = file(fPathRaw + '_LBL.csv','w')
        #Output Labeled
        for i in xrange(len(ids)):
            for dim in xrange(p+1):
                outfile.write(str(idsout[i,dim]) +',')
            outfile.write('\n')
        outfile.close()
            

        #Output plots
        if(charts == 'save' or charts == 'all' or charts == 'pdf' or charts == 'png'):
            generatePlots(fPathRaw, charts)

    #Output configuration
    outputConfiguration(fPathRaw, argsDict, cRaw)

    return

'''
    append the ids to the data, then shuffle the rows to retain data ids
'''
def shuffleRows(z, ids, sigCols):
    idsout = np.column_stack((sigCols, z))
    idsout = np.column_stack((idsout, ids))
    np.random.shuffle(idsout)
    sigCols = idsout[:,:sigCols.shape[1]]
    idsout = idsout[:,sigCols.shape[1]:]
    z = idsout[:,:-1]
    ids = idsout[:,-1:]
    return z, ids, idsout, sigCols

'''
    Transposes, shuffles columns (now rows), then transpose back for shuffled columns
'''
def shuffleCols(data):
    data = np.transpose(data)
    np.random.shuffle(data)
    data = np.transpose(data)
    return data

'''
    Run the generator from another script
'''
def runGenerator(foName, fName, argsDict):
    start = time.time()
    if foName == fName:
        fPathRaw = './' + foName + '/'
    else:
        fPathRaw = './' + foName + '/' + fName + '/'
    cRaw = ''
    for i in range(0, len(sys.argv)):
        cRaw += sys.argv[i] + ' '

    if not os.path.exists(fPathRaw):
        os.mkdir(fPathRaw)
    fPathRaw += fName

    #Parse and fill the args dictionary
    argsDict = argsDefault(argsDict)
    
    if "infile" in argsDict:  
        outfile = file(fPathRaw, 'w')  
        infile = file(argsDict["infile"],'r')

        gendata(infile,outfile,vectors)

        infile.close()
        outfile.close()
        
    else:
        z, ids, cents, sigCols = generateData(argsDict)
        
        if "shuffle" in argsDict:
            shuffle = argsDict['shuffle'][0]
            if shuffle == 'cols' or shuffle == 'all':
                z = shuffleCols(z)
            
        
        outputFiles(argsDict, fPathRaw, z, ids, cents, sigCols, cRaw)
        
        charts = argsDict['charts'][0]
        if charts == 'all' or charts == 'show':
            showPlots()
    end = time.time()
    return (end-start)
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
    
    if len(sys.argv) > 1:
    
        print "Starting generation!"
    
        for farg in sys.argv[2:]:
            (arg,val) = farg.split("=")
            argsdict[arg] = [val]
    
        runGenerator(sys.argv[1],sys.argv[1],argsdict)
        
        print "Finished!"
    
    else:
        print "Requires Outputfile [Option=<...>]\n\tSee DataGenerator.py for options and information"

'''****************************************'''

'''****************************************'''

##    python DataGenerator.py testOutput
##    python DataGenerator.py testOutput [option=value]
##    python DataGenerator.py testOutput infile=inputFile.txt vectors=100

'''*************** OPTIONS ****************

    **General Options**
        -infile (default null)	-File for input data generation
	
        -minValue (default -1)	-Max value of output data
        -maxValue (default 1)	-Min value of output data
        
        -dim (default 6)	    -Number of significant columns to generate
        -dummyCols (default 50) -Number of uncorrelated columns to generate
        
        -clusters (default 3)	-Number of clusters to generate
        -vectors (default 100)	-Number of vectors to generate

        -charts (default all) 	-Generated chart format (save, show, none, all)
    ____________________________________

    **Generation Distribution Options**
        -dist (default uniform)	-Distribution to generate points on
            -gauss or normal        -Generate points on gaussian distribution
            -uniform or uni         -Generate points uniformly
	        -binomial or binom
            -exponential or exp
    ____________________________________
   
    **CENTROID OPTIONS**
	    -corg (default random) 	-Closeness of clusters to be generated
		    -random, bi, tri, quad, all
	    -cdist (default .4) 	-Target distance of cluster centroid orgs
        -csigma (default .1)	-Deviation of a cluster
    ____________________________________

    **Output Randomization Options**
        -shuffle (default all)  (all, cols, rows, none)
    ____________________________________

```****************************************'''



import sys
from DataPlotting import *
from LeeGenerator import *
from PointGenerator import *
import os
import datetime
import numpy as np


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
def argsDefault(argsDict):
    ''' GENERATION DEFAULTS '''
    
    if not 'minValue' in argsDict:
        argsDict['minValue'] = [-1]
    if not 'maxValue' in argsDict:
        argsDict['maxValue'] = [1]
    if not 'clusters' in argsDict:
        argsDict['clusters'] = [3]
    if not 'dim' in argsDict:
        argsDict['dim'] = [6]
    if not 'vectors' in argsDict:
        argsDict['vectors'] = [100]
    if not 'dist' in argsDict:
        argsDict['dist'] = ['gauss']
    if not 'cdist' in argsDict:
        argsDict['cdist'] = [0.4]
    if not 'corg' in argsDict:
        argsDict['corg'] = ['random']
    if not 'csigma' in argsDict:
        argsDict['csigma'] = [.1]
    if not 'dummyCols' in argsDict:
        argsDict['dummyCols'] = [50]
    if not 'shuffle' in argsDict:
        argsDict['shuffle'] = ['all']
    if not 'charts' in argsDict:
        argsDict['charts'] = ['all']
    
    return argsDict
    

def generateData(argsDict):

    #Generate the data, centroids, and ids
    data, ids, cents = genRawData(argsDict)
    
    simplePlot((x[0] for x in data), (x[1] for x in data),ids,cents);
    r3DPlot((x[0] for x in data), (x[1] for x in data),(x[2] for x in data), ids,222,cents);
    r3DPlot((x[3] for x in data), (x[4] for x in data),(x[5] for x in data), ids,224,cents);
    eucPlot(data, ids,cents)
    
    data = genDummyCols(argsDict,data)

    return data, ids, cents


def outputFiles(argsDict, fPathRaw, z, ids, cents, cRaw):
    
    vectors = int(argsDict["vectors"][0])
    dimensions = int(argsDict["dim"][0])
    charts = argsDict['charts'][0]
    dummyCols = argsDict['dummyCols'][0]
    
    outfile = file(fPathRaw + '_RAW','w')

    #Output Raw
    outfile.write(str(vectors)+'\n'+str(len(z))+'\n')
    for i in xrange(len(z)):
        for dim in xrange(dimensions + dummyCols):
            outfile.write(str(z[i,dim]) + '\n')

    
    outfile = file(fPathRaw + '_LBL','w')
    #Output Labeled
    for i in xrange(len(z)):
        for dim in xrange(dimensions + dummyCols):
            outfile.write(str(z[i])+','+str(ids[i]) +'\n')

    #Output plots
    if(charts == 'save' or charts == 'all'):
        generatePlots(fPathRaw)

    #Output configuration
    outputConfiguration(fPathRaw, argsDict, cRaw)

    return


def outputConfiguration(fPathRaw, argsDict, cRaw):

    outfile = file(fPathRaw + '_CFG', 'w')
    outfile.write('******Raw Command (COPY THIS)******')
    outfile.write('\n\tpython ' + cRaw + '\n\n')

    outfile.write('******CONFIGURATION FOR GENERATION: ' + fPathRaw + ' | ')
    outfile.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +'******\n')

    outfile.write('\n' + str(argsDict).replace(',','\n').replace('{',' ').replace('}','') + '\n')

    return

def shuffleRows(z, ids):
    #TODO: need to append ids to rows so shuffle preserves ids
    return z, ids

def shuffleCols(data):
    data = np.transpose(data)
    np.random.shuffle(data)
    data = np.transpose(data)
    return data


'''****************************************'''



'''****************************************'''

'''
Main
	-Check if an input file exists
		-if so, use input file to generate the output data
		-if not, use internal method to generate the output data
'''

argsdict = {}

if len(sys.argv) > 1:

    print "Starting generation!"

    fPathRaw = './' + sys.argv[1] + '/'
    cRaw = ''
    for i in range(0, len(sys.argv)):
        cRaw += sys.argv[i] + ' '

    if not os.path.exists(fPathRaw):
        os.mkdir(fPathRaw)
    fPathRaw += sys.argv[1]


    for farg in sys.argv[3:]:
	(arg,val) = farg.split("=")
	
        argsdict[arg] = [val]

    #Parse and fill the args dictionary
    argsdict = argsDefault(argsdict)
    
    if "infile" in argsdict:  
        outfile = file(fPathRaw, 'w')  
    	infile = file(argsdict["infile"],'r')

        gendata(infile,outfile,vectors)

    	infile.close()
        outfile.close()
        
    else:
        z, ids, cents = generateData(argsdict)
    

        if "shuffle" in argsdict:
            shuffle = argsdict['shuffle'][0]
            if shuffle == 'cols' or shuffle == 'all':
                z = shuffleCols(z)
            if shuffle == 'rows' or shuffle == 'all':
                z, ids = shuffleRows(z, ids)
            
        
        outputFiles(argsdict, fPathRaw, z, ids, cents, cRaw)
        
        charts = argsdict['charts'][0]
        if charts == 'all' or charts == 'show':
            showPlots()

    print "Finished!"

else:
    print "Requires Outputfile [Option=<...>]\n\tSee DataGenerator.py for options and information"



'''****************************************'''


''' Possible (not implemented) Options:
	-noise (%)
	
	-Cluster counts weighting (currently all weights are equal)

    **Target options**
	-purity (default ?)	-Target purity of output data
	-ari	(default ?)	-Target ARI of output data
	-WCSSE	(default ?) 	-Target WCSSE of output data
	-sil	(default ?)	-Target silhouette of output data

'''

'''****************************************'''

##    python DataGenerator.py testOutput
##    python DataGenerator.py testOutput [option=value]
##    python DataGenerator.py testOutput infile=inputFile.txt vectors=100

'''*************** OPTIONS ****************

    **General Options**
        -infile (default null)	-File for input data generation
	
        -minValue (default 0)	-Max value of output data
        -maxValue (default 1)	-Min value of output data
        -dim (default 1000)	-Number of dimensions to generate
        -clusters (default 6)	-Number of clusters to generate
        -vectors (default 100)	-Number of vectors to gnerate

        -charts (default show) 	-Generated chart format (PDF, PNG, show, none)
    ____________________________________


    **Generation Distribution Options**
        -dist (default uniform)	-Distribution to generate points on
            -gauss or normal        -Generate points on gaussian distribution
            -uniform or uni         -Generate points uniformly
	    -binomial or binom
            -exponential or exp
            -

	-distMode (default ...)	-Mode to use the distribution in
		**Gaussian:
			-mu (default rand between minValue and maxValue)
			-sigma (default % of [maxValue - minValue])
		**Binomial:
		        -n (number of trials)
		        -p (probability of success)
    ____________________________________
   

    **LSH OPTIONS**
	-corg (default random) 	-Closeness of clusters to be generated
		-random, coupled, tripled, quadrupled, all
	-cdist (default .15) 	-Target distance of cluster centroids
        -csigma (default .1)	-Deviation of a cluster
    ____________________________________

        
    **Data Randomization Options**
        -shuffle rows
        -shuffle columns
    ____________________________________



```****************************************'''



import sys
from DataPlotting import *
from LeeGenerator import *
from PointGenerator import *
import os
import datetime


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
        argsDict['minValue'] = [0]
    if not 'maxValue' in argsDict:
        argsDict['maxValue'] = [10]
    if not 'clusters' in argsDict:
        argsDict['clusters'] = [3]
    if not 'dim' in argsDict:
        argsDict['dim'] = [6]
    if not 'vectors' in argsDict:
        argsDict['vectors'] = [100]
    if not 'dist' in argsDict:
        argsDict['dist'] = ['gauss']
    if not 'cdist' in argsDict:
        argsDict['cdist'] = [0.15]
    if not 'csigma' in argsDict:
        argsDict['csigma'] = [.1]
    
    return argsDict
    

def generateData(argsDict):
    #Parse and fill the args dictionary
    argsDict = argsDefault(argsDict)

    #Generate the data, centroids, and ids
    data, ids, cents = genRawData(argsDict);
    
    simplePlot((x[0] for x in data), (x[1] for x in data),ids,cents);
    r3DPlot((x[0] for x in data), (x[1] for x in data),(x[2] for x in data), ids,222,cents);
    r3DPlot((x[3] for x in data), (x[4] for x in data),(x[5] for x in data), ids,224,cents);
    eucPlot(data, ids,cents)

    return data, ids, cents


def outputFiles(argsDict, fPathRaw, z, ids, cents, cRaw):
    
    vectors = int(argsDict["vectors"][0])
    dimensions = int(argsDict["dim"][0])
    
    outfile = file(fPathRaw + '_RAW','w')

    #Output Raw
    outfile.write(str(vectors)+'\n'+str(len(z))+'\n')
    for i in xrange(len(z)):
        for dim in xrange(dimensions):
            outfile.write(str(z[i,dim]) + '\n')

    
    outfile = file(fPathRaw + '_LBL','w')
    #Output Labeled
    for i in xrange(len(z)):
        for dim in xrange(dimensions):
            outfile.write(str(z[i])+','+str(ids[i]) +'\n')

    #Output plots
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
    return

def shuffleCols(z):
    np.transpose(z)
    np.random.shuffle(z)
    np.transpose(z)
    return


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

    fPathRaw = './' + sys.argv[1] + '/'
    cRaw = ''
    for i in range(0, len(sys.argv)):
        cRaw += sys.argv[i] + ' '

    if not os.path.exists(fPathRaw):
        os.mkdir(fPathRaw)
    fPathRaw += sys.argv[1]


    size = 100

    for farg in sys.argv[3:]:
	(arg,val) = farg.split("=")
	
        argsdict[arg] = [val]

    OUTPUT_MAT_ONLY = len(sys.argv)>3 and bool(sys.argv[3])

    if "vectors" in argsdict:
        size = int(argsdict['vectors'][0])
    if "infile" in argsdict:  
        outfile = file(fPathRaw, 'w')  
    	infile = file(argsdict["infile"],'r')

	gendata(infile,outfile,size)

    	infile.close()
        outfile.close()
    else:
        z, ids, cents = generateData(argsdict)
        outputFiles(argsdict, fPathRaw, z, ids, cents, cRaw)

    showPlots()

    print "Finished!"

else:
    print "Requires Outputfile [Option=<...>]\n\tSee DataGenerator.py for options and information"







'''****************************************'''


''' Possible (not implemented) Options:
	-noise (%)

	-order 	(default none)	-Order of generated points (may affect tree creation if ordered by clusters (stacking the deck))

    **Target options**
	-purity (default ?)	-Target purity of output data
	-ari	(default ?)	-Target ARI of output data
	-WCSSE	(default ?) 	-Target WCSSE of output data
	-sil	(default ?)	-Target silhouette of output data

'''

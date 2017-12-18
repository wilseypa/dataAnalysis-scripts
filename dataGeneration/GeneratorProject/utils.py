import datetime
from DataPlotting import *
import csv

'''************** AUTHOR NICK *************'''

def argsDefault(argsDict):
    ''' GENERATION DEFAULTS '''
    
    if not 'minValue' in argsDict:  #DEFAULT  -.999
        argsDict['minValue'] = [-.999]
    if not 'maxValue' in argsDict:  #DEFAULT .999
        argsDict['maxValue'] = [.999]
    if not 'scaling' in argsDict:  #DEFAULT 'true'
        argsDict['scaling'] = ['true']
 
    if not 'centroidFile' in argsDict:
	argsDict['centroidFile'] = None
    if not 'clusters' in argsDict:  #DEFAULT 3
        argsDict['clusters'] = [3]
    if not 'dim' in argsDict:  #DEFAULT 100
        argsDict['dim'] = [100]
    if not 'vectors' in argsDict:  #DEFAULT 500
        argsDict['vectors'] = [500]
    
    if not 'dist' in argsDict:  #DEFAULT 'gauss'
        argsDict['dist'] = ['gauss']
    if not 'cdist' in argsDict:  #DEFAULT .4
        argsDict['cdist'] = [0.4]
    if not 'corg' in argsDict:  #DEFAULT 'random'
        argsDict['corg'] = ['random']
    if not 'csigma' in argsDict:  #DEFAULT .1
        argsDict['csigma'] = [.1]
    if not 'ccounts' in argsDict:  #DEFAULT 'random'
        argsDict['ccounts'] = ['random']
    
    if not 'ext' in argsDict:  #DEFAULT 'all'
        argsDict['ext'] = ['all']
    if not 'exec' in argsDict:  #DEFAULT 'cluster'
        argsDict['exec'] = ['cluster']
        
    if not 'evolve' in argsDict:  #DEFAULT 'false'
        argsDict['evolve'] = ['false']
    if not 'evint' in argsDict:  #DEFAULT 50
        argsDict['evint'] = [50]
    if not 'evtype' in argsDict:  #DEFAULT 'random'
        argsDict['evtype'] = ['random']
        
    if not 'charts' in argsDict:  #DEFAULT 'pdf'
        argsDict['charts'] = ['pdf']
    if not 'output' in argsDict: #DEFAULT 'all'
        argsDict['output'] = ['all']
    if not 'param' in argsDict: #DEFAULT 'vectors'
        argsDict['param'] = ['vectors']
        
    if not 'multithread' in argsDict:   #DEFAULT 'false'
        argsDict['multithread'] = ['false']
    if not 'threads' in argsDict:   #DEFAULT 2
        argsDict['threads'] = [2]
    if not 'multirun' in argsDict: #DEFAULT 5
        argsDict['multirun'] = [5]
    if not 'batches' in argsDict: #DEFAULT 2
        argsDict['batches'] = [2]
        
    if not 'rshuf' in argsDict:  #DEFAULT 'true'
        argsDict['rshuf'] = ['true']
    if not 'cshuf' in argsDict:  #DEFAULT 'random'
        argsDict['cshuf'] = ['random']
    if not 'featnoise' in argsDict: # DEFAULT 0
        argsDict['featnoise'] = [0.00]
    if not 'vectnoise' in argsDict: # DEFAULT 0
        argsDict['vectnoise'] = [0.00]
    if not 'noise' in argsDict:  #DEFAULT 0
        argsDict['noise'] = [.00]
        
        
    ''' DEFAULTS RPHash Params'''
    
    if not 'parallel' in argsDict:  #DEFAULT 'true'
        argsDict['parallel'] = ['true']
    if not 'decodertype' in argsDict:  #DEFAULT 'none'
        argsDict['decodertype'] = ['adaptive']
    if not 'numprojections' in argsDict:  #DEFAULT 0
        argsDict['numprojections'] = [1]
    if not 'numblur' in argsDict:  #DEFAULT 0
        argsDict['numblur'] = [1]
    if not 'runs' in argsDict:  #DEFAULT 1
        argsDict['runs'] = [1]
    if not 'clusteringmethod' in argsDict:  #DEFAULT 'adaptive'
        argsDict['clusteringmethod'] = ['adaptive']
    if not 'offlineclusterer' in argsDict:  #DEFAULT 'none'
        argsDict['offlineclusterer'] = ['none']
    if not 'dimparameter' in argsDict:  #DEFAULT 24
        argsDict['dimparameter'] = [24]
    if not 'projection' in argsDict: #DEFAULT 'dbf'
        argsDict['projection'] = ['dbf']

    return argsDict

def readDataFromFile(rawFileName, type):
    result = csv.reader(open(rawFileName,"rb"),delimiter=',')
    result = np.array(list(result)).astype('float')
    return result.astype(type)


def generateChart(data, lbls, input, mapping):
    match = {}
    inC = {}
    
    if len(mapping) >0:  
        for i in xrange(len(input)):
            if int(input[i]) < len(mapping):
                inC[i] = int(mapping[int(input[i])])
                if int(lbls[i]) == int(mapping[int(input[i])]):
                    match[i] = 0;
                else:
                    match[i]=1
            else:
                inC[i] = int(input[i])
                match[i] = 1;
        cents = []
        clearPlots()
        simplePlot((x[0] for x in data), (x[1] for x in data),inC,cents, match);
        r3DPlot((x[0] for x in data), (x[1] for x in data),(x[2] for x in data), inC,222,cents, match);
        r3DPlot((x[3] for x in data), (x[4] for x in data),(x[5] for x in data), inC,224,cents, match);
        eucPlot(data, inC,cents, match)
    
    return


def outputConfiguration(fPathRaw, argsDict, cRaw):

    outfile = file(fPathRaw + '_CFG', 'w')
    outfile.write('******Raw Command (COPY THIS)******')
    outfile.write('\n\tpython ' + cRaw + '\n\n')

    outfile.write('******CONFIGURATION FOR GENERATION: ' + fPathRaw + ' | ')
    outfile.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +'******\n')

    outfile.write('\n' + str(argsDict).replace(',','\n').replace('{',' ').replace('}','') + '\n')

    return


'''****************************************'''

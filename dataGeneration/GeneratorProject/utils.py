import datetime
from DataPlotting import *


def argsDefault(argsDict):
    ''' GENERATION DEFAULTS '''
    
    if not 'minValue' in argsDict:  #DEFAULT  -.999
        argsDict['minValue'] = [-.999]
    if not 'maxValue' in argsDict:  #DEFAULT .999
        argsDict['maxValue'] = [.9999]
    if not 'scaling' in argsDict:  #DEFAULT 'true'
        argsDict['scaling'] = ['true']
    if not 'clusters' in argsDict:  #DEFAULT 3
        argsDict['clusters'] = [3]
    if not 'dim' in argsDict:  #DEFAULT 100
        argsDict['dim'] = [100]
    if not 'vectors' in argsDict:  #DEFAULT 1000
        argsDict['vectors'] = [1000]
    if not 'dist' in argsDict:  #DEFAULT 'gauss'
        argsDict['dist'] = ['gauss']
    if not 'cdist' in argsDict:  #DEFAULT .4
        argsDict['cdist'] = [0.4]
    if not 'corg' in argsDict:  #DEFAULT random
        argsDict['corg'] = ['random']
    if not 'csigma' in argsDict:  #DEFAULT .1
        argsDict['csigma'] = [.1]
    if not 'dummyCols' in argsDict:  #DEFAULT 50
        argsDict['dummyCols'] = [50]
    if not 'rshuf' in argsDict:  #DEFAULT 'true'
        argsDict['rshuf'] = ['true']
    if not 'cshuf' in argsDict:  #DEFAULT 'random'
        argsDict['cshuf'] = ['random']
    if not 'charts' in argsDict:  #DEFAULT 'pdf'
        argsDict['charts'] = ['pdf']
    if not 'ccounts' in argsDict:  #DEFAULT 'random'
        argsDict['ccounts'] = ['random']
    if not 'noise' in argsDict:  #DEFAULT 0
        argsDict['noise'] = [0]
    
    return argsDict

def generateChart(data, lbls, input, mapping):
    match = {}
    inC = {}
    
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
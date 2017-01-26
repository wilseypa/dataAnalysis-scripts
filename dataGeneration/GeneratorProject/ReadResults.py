'''****************************************'''

##    python ReadResults.py data_LBL output_RAW resultsFile.csv
##    python ReadResults.py <LBL data> <Tested data> <Results> <Option=value>

'''*************** OPTIONS ****************

    

```****************************************'''
from DataPlotting import *
import sys
import csv
import os
import datetime
import numpy as np


'''
Notes:
    -Data analyzer for comparing generated data and test output

'''

'''************** AUTHOR NICK *************'''

def calcPurity(ids, input, mapping):
    bcid = np.bincount(ids) 
    bcin = np.bincount(input[:,0])
    count = 0
    
    for i in xrange(len(input)):
        if int(input[i]) < len(mapping):
            if int(ids[i]) == int(mapping[int(input[i])]):
                count += 1
    
    purity = count/float(len(input))
    print "\tRun Purity: " + str(purity)
    if purity == 0.0:
        print bcid
        print bcin
    
    return purity

def readInputFromFile(rawFileName):
    infile = file(rawFileName,'r')
    
    vects = infile.readline()
    cols = infile.readline()
    
    zf = []
    
    for v in xrange(int(vects)):
        zi = []
        
        for c in xrange(int(cols)):
            z = [float(infile.readline())]
            
            if(zi == []):
                zi = z
            else:
                zi = np.hstack((zi,z))
                
        if(zf == []):
            zf = zi
        else:
            zf = np.vstack((zf,zi))
            
    return zf.astype(int)
    

def readDataFromFile(rawFileName, type):
    result = csv.reader(open(rawFileName,"rb"),delimiter=',')
    result = np.array(list(result)).astype('float')
    return result.astype(type)


def argsDefault(argsDict):
    ''' GENERATION DEFAULTS '''
    
    if not 'charts' in argsDict:
        argsDict['charts'] = ['pdf']
    
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
    
    
def mapIdstoInput(ids, input):
    #Lazy way of doing this - rework?
    mapping =[]
    #print np.amin(ids)
    #print np.amax(ids)
    #print np.amin(input)
    #print np.amax(input)
    
    #print np.bincount(ids) 
    #print np.bincount(input[:,0])
    for i in range(0,np.amax(input) + 1):
        current = {}
        for z in xrange(len(input)):
            if(input[z] == i):
                if int(ids[z]) in current:
                    current[int(ids[z])] = current[int(ids[z])] + 1;
                else:
                    current[int(ids[z])] = 1
        max = 0
        maxI = 0
        print "\t" + str(i) + ": " + str(current)
        for z in current:
            if(current[z] > max):
                max = int(current[z])
                maxI = z
        if mapping == []:
            mapping = np.array([maxI])
        else:
            mapping = np.vstack((mapping,[maxI]))
    
    return mapping
    

def outputFiles(argsDict, fPathRaw, cRaw):
        
    charts = argsDict['charts'][0]
        
    outfile = file(fPathRaw,'w')
    #outfile.write(str(len(ids)) + '\n')
    #Output Labeled
    #for i in xrange(len(ids)):
    #    for dim in xrange(p+1):
    #        outfile.write(str(idsout[i,dim]) +',')
    #    outfile.write('\n')

    #Output plots
    if(charts == 'save' or charts == 'all' or charts == 'pdf' or charts == 'png'):
        generatePlots(fPathRaw, charts)

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


def runAnalysis(lblPathRaw, inputPathRaw, outPathRaw, sigColsPath):
    argsdict = {}
    
    ids = readDataFromFile(lblPathRaw, 'int')
    sigCols = readDataFromFile(sigColsPath, 'float')
    input = readInputFromFile(inputPathRaw)
    cRaw = ''
    ids = ids[2:,-1]
    zf = []
    
    #Parse and fill the args dictionary
    argsdict = argsDefault(argsdict)
    mapping = mapIdstoInput(ids, input)
    purity = calcPurity(ids, input, mapping)
    generateChart(sigCols, ids, input, mapping)
    #showPlots()
    outputFiles(argsdict, outPathRaw,cRaw)
    charts = argsdict['charts'][0]
    if charts == 'all' or charts == 'show':
        showPlots()
    
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
    
        print "Starting results analysis!"
        
        lblPathRaw = sys.argv[1]
        inputPathRaw = sys.argv[2]
        
        lbls = readDataFromFile(lblPathRaw)
        input = readInputFromFile(inputPathRaw)
        
        
        data = lbls[:,1:-1]
        lbls = lbls[:,-1]
        zf = []
        for row in data:
            dataEuc = np.linalg.norm(row)
            if(zf == []):
                zf = [dataEuc];
            else:
                zf= np.vstack((zf,dataEuc))
    
        outPathRaw = './' + sys.argv[3] + '/'
        cRaw = ''
        for i in range(0, len(sys.argv)):
            cRaw += sys.argv[i] + ' '
        if not os.path.exists(outPathRaw):
            os.mkdir(outPathRaw)
        outPathRaw += sys.argv[3]
    
    
        for farg in sys.argv[4:]:
            (arg,val) = farg.split("=")
        
            argsdict[arg] = [val]
    
        #Parse and fill the args dictionary
        argsdict = argsDefault(argsdict)
        
        outputFiles(argsdict, outPathRaw,cRaw)
            
        charts = argsdict['charts'][0]
        #if charts == 'all' or charts == 'show':
            #showPlots()
    
        print "Finished!"
    
    else:
        print "Requires Outputfile [Option=<...>]\n\tSee DataGenerator.py for options and information"



'''****************************************'''


''' Possible (not implemented) Options:
    -noise (%)
    
    -Cluster counts weighting (currently all weights are equal)

    **Target options**
    -purity (default ?)    -Target purity of output data
    -ari    (default ?)    -Target ARI of output data
    -WCSSE    (default ?)     -Target WCSSE of output data
    -sil    (default ?)    -Target silhouette of output data

'''

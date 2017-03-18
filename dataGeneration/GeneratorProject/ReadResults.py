'''****************************************'''

##    python ReadResults.py data_LBL output_RAW resultsFile.csv
##    python ReadResults.py <LBL data> <Tested data> <Results> <Option=value>

'''*************** OPTIONS ****************

    **General Options**
        -charts (default pdf)     -Generated chart format (save, show, none, all, png, pdf)
    
```****************************************'''
from DataPlotting import *
from utils import *
from stats import *
import sys
import os
import datetime
import time


'''
Notes:
    -Data analyzer for comparing generated data and test output

'''

'''************** AUTHOR NICK *************'''

'''
    Read raw input from file
'''
def readInputFromFile(rawFileName, type):
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
    infile.close()
    return zf.astype(type)
    

'''
    Map the input ids to the ground truth ids 
'''
def mapIdstoInput(ids, input):
    #Lazy way of doing this - rework?
    mapping =[]
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
        for z in current:
            if(current[z] > max):
                max = int(current[z])
                maxI = z
        if mapping == []:
            mapping = np.array([maxI])
        else:
            mapping = np.vstack((mapping,[maxI]))
    
    return mapping
    
'''
    Output the results, configuration, plot files to the file path 
'''
def outputFiles(argsDict, fPathRaw, cRaw):
        
    charts = argsDict['charts'][0]
        
    #outfile = file(fPathRaw,'w')
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

def runRawAnalysis(argsdict,lbls,inputs,outPathRaw,sigColsPath, tt):
    start = time.time()
    
    sigCols = readDataFromFile(sigColsPath, 'float')
    cRaw = ''
    zf = []
    
    #mapping = mapIdstoInput(lbls, inputs)
    mapping = {}
    ari,nmi,ami,homogeneity,completeness,vscore,fmi = calcCentroidMetrics(lbls,inputs,mapping)
    generateChart(sigCols, lbls, inputs, mapping)
    #showPlots()
    outputFiles(argsdict, outPathRaw,cRaw)
    charts = argsdict['charts'][0]
    if charts == 'all' or charts == 'show':
        showPlots()
    end = time.time()
    return ari,nmi,ami,homogeneity,completeness,vscore,fmi,(end - start), tt



'''
    Run the analysis on output labels and ground truths
'''
def runAnalysis(argsdict,lbls,inputs,outPathRaw,sigColsPath, tt):
    start = time.time()
    
    sigCols = readDataFromFile(sigColsPath, 'float')
    lbls = readDataFromFile(lbls,'int')
    inputs = readDataFromFile(inputs,'int')
    
    cRaw = ''
    zf = []
    
    #mapping = mapIdstoInput(lbls, inputs)
    mapping = {}
    ari,nmi,ami,homogeneity,completeness,vscore,fmi = calcCentroidMetrics(lbls,inputs,mapping)
    generateChart(sigCols, lbls, inputs, mapping)
    #showPlots()
    
    outputFiles(argsdict, outPathRaw,cRaw)
    charts = argsdict['charts'][0]
    if charts == 'all' or charts == 'show':
        showPlots()
    end = time.time()
    return ari,nmi,ami,homogeneity,completeness,vscore,fmi,(end - start), tt


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
        
        lbls = readDataFromFile(lblPathRaw, 'float')
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

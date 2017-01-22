'''****************************************'''

##    python ReadResults.py data_LBL output_RAW resultsFile.csv
##    python ReadResults.py <LBL data> <Tested data> <Results> <Option=value>

'''*************** OPTIONS ****************

    

```****************************************'''
#from ..GeneratorProject import PointGenerator
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
            
    print zf
    return zf
    

def readDataFromFile(rawFileName):
    result = csv.reader(open(rawFileName,"rb"),delimiter=',')
    result = np.array(list(result)).astype('float')
    
    return result


def argsDefault(argsDict):
    ''' GENERATION DEFAULTS '''
    
    if not 'charts' in argsDict:
        argsDict['charts'] = ['all']
    
    return argsDict



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
    if(charts == 'save' or charts == 'all'):
        #generatePlots(fPathRaw)
        print(' ')

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


'''****************************************'''



'''****************************************'''

'''
Main
    -Check if an input file exists
        -if so, use input file to generate the output data
        -if not, use internal method to generate the output data
'''

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
    print zf

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

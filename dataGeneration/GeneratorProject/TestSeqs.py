'''****************************************'''

##    python TestSeqs.py overlap overlapTestFiles
##    python TestSeqs.py [testType] [outputFolder] [option=value]
##    python TestSeqs.py overlap overlapTestFiles vectors=10000 dim=1000

'''*************** OPTIONS ****************

    **General Options**
        -exec (default all)    -Determine what programs to use for analysis
                                'all' - use RPHash and LSHKit (see req's)
                                    'rphash', 'lshkit', 'none'
                                    'cluster': rphash + sklearn
                                    'LSH': rphash + lshkit
    
        -infile (default null)    -File for input data generation
    
        -scaling (default true)     -Toggle scaling of generated data
        -minValue (default -.999)    -Max value of output data
        -maxValue (default .999)    -Min value of output data
        
        -dim (default 100)        -Number of significant columns to generate
        -dummyCols (default 50) -Number of uncorrelated columns to generate
        
        -clusters (default 3)    -Number of clusters to generate
        -vectors (default 1000)    -Number of vectors to generate

        -charts (default pdf)     -Generated chart format (save, show, none, all, png, pdf)
    ____________________________________

    **Generation Distribution Options**
        -dist (default gauss)    -Distribution to generate points on
            -gauss or normal        -Generate points on gaussian distribution
            -uniform or uni         -Generate points uniformly
            -binomial or binom      -Generate points using a binomial distribution
            -exponential or exp     -Generate points using an exponential distribution
    ____________________________________
   
    **CENTROID OPTIONS**
        -corg (default random)     -Organization of clusters to be generated (pairs, triplets, etc.)
                                    -random, bi, tri, quad, all
        -cdist (default .4)     -Target distance of cluster centroid orgs
        -csigma (default .1)    -Deviation of a cluster
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
        -noise (default 0%) (0-1)  -TODO Amount of noise to add to final output
    ____________________________________

```****************************************'''

from MultiRun import *
import glob
from itertools import islice


'''************** AUTHOR NICK *************'''

'''
    Run a dimension test, varying the significant dimensions from 50 to 1000
'''
def dimensionTest(argsDict, foName):
    results = ''
    
    if not os.path.exists('./' + foName + '/'):
        os.mkdir('./' + foName + '/')
    
    for i in range(0, 20):
        argsDict['dim'] = [(20-i) * 50]
        runMultiRun(argsDict, foName + '/' + foName + str(i), foName + str(i), 5, 'DIM='+str(argsDict['dim'][0]))
        results = aggResults(argsDict, foName, results, i)

    outfile = file('./' + foName + '/RESULTS_DIMTEST.csv', 'w')
    outfile.write(results)
    outfile.close()
    return

'''
    Run an overlap test, varying the cluster distance from 5 to .5
'''
def overlapTest(argsDict, foName):
    argsDict['clusters'] = [2]
    argsDict['csigma'] = [.05]
    argsDict['corg'] = ['bi']
    results = ''
    if not os.path.exists('./' + foName + '/'):
        os.mkdir('./' + foName + '/')
    
    for i in range(0, 10):
        argsDict['cdist'] = [.5 * (i + 1)]
        runMultiRun(argsDict, foName + '/' + foName + str(i), foName + str(i), 5, 'CDIST='+str(argsDict['cdist'][0]))
        results = aggResults(argsDict, foName, results, i)

    outfile = file('./' + foName + '/RESULTS_OVERLAP.csv', 'w')
    outfile.write(results)
    outfile.close()
    return

'''
    Run a column noise test, varying the significant dimensions from 1000/1000 to 0/1000
'''
def colNoiseTest(argsDict, foName):
    v = 1000
    
    results = ''
    if not os.path.exists('./' + foName + '/'):
        os.mkdir('./' + foName + '/')
    
    for i in range(0, 11):
        c = int((10-i) * v/10)
        argsDict['dim'][0] = c
        argsDict['dummyCols'][0] = int(v - c)
        runMultiRun(argsDict, foName + '/' + foName + str(i), foName + str(i), 5, 'dim='+str(argsDict['dim'][0]))
        results = aggResults(argsDict, foName, results, i)

    outfile = file('./' + foName + '/RESULTS_COLNOISE.csv', 'w')
    outfile.write(results)
    outfile.close()
    return

'''
    Aggregate the multirun result files
        TODO: Continuous file write for testing in case of exception
'''
def aggResults(argsDict, foName, results,i):
    r = glob.glob(('./' + foName + '/' + foName + str(i) + '/*.csv'))
    if os.path.isfile(r[0]):
        out = file(r[0], 'r')
        if results == '':
            results = out.read()
        else:
            currentLine = out.readlines()[1:]
            for line in currentLine:
                results = results + line
        out.close()
    return results

'''
Main
    -Check if an input file exists
        -if so, use input file to generate the output data
        -if not, use internal method to generate the output data
'''
if __name__ == "__main__":
    
    argsdict = {}
    if len(sys.argv) > 2:
        testType = sys.argv[1]
        print os.getcwd()
        print "Starting Test Generation and Analysis for " + testType
    
        foName = sys.argv[2]
        cRaw = ''
        for i in range(0, len(sys.argv)):
            cRaw += sys.argv[i] + ' '
            
        for farg in sys.argv[3:]:
            (arg,val) = farg.split("=")
        
            argsdict[arg] = [val]
            
        argsdict = argsDefault(argsdict)
        if testType == 'overlap':
            overlapTest(argsdict, foName)
        if testType == 'dim' or testType == 'dimension' or testType == 'dimensional':
            dimensionTest(argsdict,foName)
        if testType == 'col' or testType == 'colNoise':
            colNoiseTest(argsdict, foName)
            
    else:
        print "Requires [testType] [outputFolder] [Option=<...>]\n\tSee TestSeqs.py for options and information"

        
'''****************************************'''
    
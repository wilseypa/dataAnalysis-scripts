'''****************************************'''

##    python TestSeqs.py 3_5_17 overlap dim charts='none'
##    python TestSeqs.py [testLabel] [test1 test2 ...] [option=value]
##    python TestSeqs.py overlap overlapTestFiles vectors=10000 dim=1000

'''*************** OPTIONS ****************

    **General Options**
        -exec (default all)    -Determine what programs to use for analysis
                                'all' - use RPHash, sklearn, and LSHKit (see req's in readme)
                                'rphash' 
                                'lshkit' 
                                'cluster': rphash + sklearn
                                'LSH': rphash + lshkit
                                'none'
    
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
    argsDict['dummyCols'] = [0]
    argsDict['vectors'] = [500]
    argsdict['param']=['dim']
    
    if not os.path.exists('./' + foName + '/'):
        os.mkdir('./' + foName + '/')
    
    #Jump in 5's until 50
    for i in range(1,11):
        argsDict['dim'] = [i * 5]
        runMultiRun(argsDict, foName + '/' + foName + str(i), foName + str(i), 2, 'DIM='+str(argsDict['dim'][0]))
        results = aggResults(argsDict, foName, results, i)
        
    outfile = file('./' + foName + '/RESULTS_DIMTEST.csv', 'w')
    outfile.write(results)
    outfile.close()
    
    #Jump in 50's until 1000
    for i in range(1, 21):
        argsDict['dim'] = [i * 50]
        runMultiRun(argsDict, foName + '/' + foName + str(i+10), foName + str(i+10), 2, 'DIM='+str(argsDict['dim'][0]))
        results = aggResults(argsDict, foName, results, i+10)
    
    outfile = file('./' + foName + '/RESULTS_DIMTEST.csv', 'w')
    outfile.write(results)
    outfile.close()
    
    #Jump in 500's until 5000
    for i in range(3, 11):
        argsDict['dim'] = [i * 500]
        runMultiRun(argsDict, foName + '/' + foName + str(i+30), foName + str(i+30), 2, 'DIM='+str(argsDict['dim'][0]))
        results = aggResults(argsDict, foName, results, i+30)
    
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
    argsdict['param']=['cdist']
    results = ''
    if not os.path.exists('./' + foName + '/'):
        os.mkdir('./' + foName + '/')
    
    for i in range(0, 21):
        argsDict['cdist'] = [.5 * (i + 1)]
        runMultiRun(argsDict, foName + '/' + foName + str(i), foName + str(i), 2, 'CDIST='+str(argsDict['cdist'][0]))
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
    argsdict['param']=['dim']
    results = ''
    if not os.path.exists('./' + foName + '/'):
        os.mkdir('./' + foName + '/')
    
    for i in range(0, 1):
        c = int((10-i) * v/10)
        argsDict['dim'][0] = c
        argsDict['dummyCols'][0] = int(v - c)
        runMultiRun(argsDict, foName + '/' + foName + str(i), foName + str(i), 2, 'dim='+str(argsDict['dim'][0]))
        results = aggResults(argsDict, foName, results, i)

    outfile = file('./' + foName + '/RESULTS_COLNOISE.csv', 'w')
    outfile.write(results)
    outfile.close()
    return

'''
    Run a random noise test
'''
def noiseTest(argsDict, foName):
    results = ''
    argsDict['vectors'] = [250]
    argsDict['dim'] = [250]
    argsdict['param']=['noise']
    
    if not os.path.exists('./' + foName + '/'):
        os.mkdir('./' + foName + '/')
    
    #Jump in .2's starting at 0 until .20
    for i in range(0,11):
        argsDict['noise'] = [double(i*2)/100.0]
        runMultiRun(argsDict, foName + '/' + foName + str(i), foName + str(i), 2, 'noise='+str(argsDict['noise'][0]))
        results = aggResults(argsDict, foName, results, i)

    outfile = file('./' + foName + '/RESULTS_NOISETEST.csv', 'w')
    outfile.write(results)
    outfile.close()
    
    #Jump in .5's starting at .25 until 1.00
    for i in range(5, 21):
        argsDict['noise'] = [double(i * 5)/100.0]
        runMultiRun(argsDict, foName + '/' + foName + str(i+10), foName + str(i+10), 2, 'noise='+str(argsDict['noise'][0]))
        results = aggResults(argsDict, foName, results, i+10)
    
    outfile = file('./' + foName + '/RESULTS_NOISETEST.csv', 'w')
    outfile.write(results)
    outfile.close()
   
    
    return



'''
    Run a column noise test, varying the significant dimensions from 1000/1000 to 0/1000
'''
def vectorTest(argsDict, foName):
    results = ''
    argsDict['dummyCols'] = [0]
    argsDict['dim'] = [500]
    
    if not os.path.exists('./' + foName + '/'):
        os.mkdir('./' + foName + '/')
    
    #Jump in 5's until 50
    for i in range(2,11):
        argsDict['vectors'] = [i * 5]
        runMultiRun(argsDict, foName + '/' + foName + str(i), foName + str(i), 2, 'vect='+str(argsDict['vectors'][0]))
        results = aggResults(argsDict, foName, results, i)

    outfile = file('./' + foName + '/RESULTS_VECTTEST.csv', 'w')
    outfile.write(results)
    outfile.close()
    
    #Jump in 50's until 1000
    for i in range(1, 21):
        argsDict['vectors'] = [i * 50]
        runMultiRun(argsDict, foName + '/' + foName + str(i+10), foName + str(i+10), 2, 'vect='+str(argsDict['vectors'][0]))
        results = aggResults(argsDict, foName, results, i+10)
    
    outfile = file('./' + foName + '/RESULTS_VECTTEST.csv', 'w')
    outfile.write(results)
    outfile.close()
    
    #Jump in 500's until 5000
    for i in range(3, 11):
        argsDict['vectors'] = [i * 500]
        runMultiRun(argsDict, foName + '/' + foName + str(i+30), foName + str(i+30), 2, 'vect='+str(argsDict['vectors'][0]))
        results = aggResults(argsDict, foName, results, i+30)
    
    outfile = file('./' + foName + '/RESULTS_VECTTEST.csv', 'w')
    outfile.write(results)
    outfile.close()
    
    return

'''
    Run a column noise test, varying the significant dimensions from 1000/1000 to 0/1000
'''
def clustsTest(argsDict, foName):
    results = ''
    argsDict['vectors'] = [250]
    argsDict['dim'] = [250]
    argsdict['param']=['clusters']
    
    if not os.path.exists('./' + foName + '/'):
        os.mkdir('./' + foName + '/')
    
    #Jump in 1's starting at 2 until 10
    for i in range(2,11):
        argsDict['clusters'] = [i]
        runMultiRun(argsDict, foName + '/' + foName + str(i), foName + str(i), 2, 'clusters='+str(argsDict['clusters'][0]))
        results = aggResults(argsDict, foName, results, i)

    outfile = file('./' + foName + '/RESULTS_CLUSTSTEST.csv', 'w')
    outfile.write(results)
    outfile.close()
    
    #Jump in 3's starting at 10 until 40
    for i in range(1, 11):
        argsDict['clusters'] = [(i * 3) + 10]
        runMultiRun(argsDict, foName + '/' + foName + str(i+10), foName + str(i+10), 2, 'clusters='+str(argsDict['clusters'][0]))
        results = aggResults(argsDict, foName, results, i+10)
    
    outfile = file('./' + foName + '/RESULTS_CLUSTSTEST.csv', 'w')
    outfile.write(results)
    outfile.close()
    
    #Jump in 10's until 100
    for i in range(1, 7):
        argsDict['clusters'] = [(i * 10) + 40]
        runMultiRun(argsDict, foName + '/' + foName + str(i+30), foName + str(i+30), 2, 'clusters='+str(argsDict['clusters'][0]))
        results = aggResults(argsDict, foName, results, i+30)
    
    outfile = file('./' + foName + '/RESULTS_CLUSTSTEST.csv', 'w')
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
    if len(sys.argv) >= 2:
        testType = []
        for farg in sys.argv[2:]:
            if not '=' in farg:
                testType.append(farg)
            else:
                (arg,val) = farg.split("=")
        
                argsdict[arg] = [val]
                
        print os.getcwd()
        print "Starting Test Generation and Analysis for " + str(testType)
    
        cRaw = ''
        for i in range(0, len(sys.argv)):
            cRaw += sys.argv[i] + ' '            
        fn = sys.argv[1]
        argsdict = argsDefault(argsdict)
        if 'noise' in testType or 'all' in testType:
            foName = fn + '.noise'
            noiseTest(argsdict,foName)
        if 'dim' in testType or 'all' in testType:
            foName = fn + '.dim'
            dimensionTest(argsdict,foName)
        if 'vect' in testType or 'all' in testType:
            foName = fn + '.vect'
            vectorTest(argsdict,foName)
        if 'overlap' in testType or 'all' in testType:
            foName = fn + '.overlap'
            overlapTest(argsdict, foName)
        if 'col' in testType or 'all' in testType:
            foName = fn + '.noise'
            colNoiseTest(argsdict, foName)
        if 'clusts' in testType or 'all' in testType:
            foName = fn + '.clusts'
            clustsTest(argsdict,foName)
            
    else:
        print "Requires [testType] [outputFolder] [Option=<...>]\n\tSee TestSeqs.py for options and information"

        
'''****************************************'''
    
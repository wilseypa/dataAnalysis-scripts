'''****************************************'''

##    python TestSeqs.py 3_5_17 overlap dim charts='none'
##    python TestSeqs.py [testLabel] [test1 test2 ...] [option=value]
##    python TestSeqs.py overlap overlapTestFiles vectors=10000 dim=1000

##    Current Test Labels: 'all', 'vectnoise', 'colnoise', 'randnoise',
##                         'dim', 'vect', 'clusts', 'var', 'overlap'

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
        -minValue (default -.999)   -Max value of output data
        -maxValue (default .999)    -Min value of output data
        
        -clusters (default 3)     -Number of clusters to generate
        -vectors (default 1000)   -Number of vectors to generate
        -dim (default 100)        -Number of significant columns to generate

        -charts (default pdf)        -Generated chart format (save, show, none, all, png, pdf)
        -output (default all)        -Output 'all' or 'minimal' files (generator)
        -param  (default 'vectors')  -Parameter to add to csv output; can be any other parameter
    ____________________________________
    
    **Noise Options**
        -noise (default 0%) (0-1)      -Amount of noise to add to final output
        -featnoise (default 0%) (0-1)   -Percentage of uncorrelated features to generate
        -vectnoise (default 0%) (0-1)  -Percentage of uncorrelated vectors to generate
    ___________________________________

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
        -cdist (default .4)        -Target distance of cluster centroid orgs
        -csigma (default .1)       -Deviation of a cluster
        -ccounts (default random)  -Cluster counts to partition total vectors into
                                       -random, equal, (TODO)separated
    ____________________________________
    
    **Test Sequence Multithreading**
        -multithread (default false)    -Run multithreaded test sequences (python limits 1 sequence per core)
        -threads (default 2)            -Max number of threads to spawn
    ____________________________________

    **Output Randomization Options**
        -rshuf (default true)  (true, false) -Randomize the vectors (Rows)
        -cshuf (default random) (separated, intermixed, random)
                                    -Determine how to shuffle the columns; separated keeps significant
                                        columns stacked on low indexed features and dummy columns on 
                                        high indexed features; intermixed disperses evenly; random
                                        performs a shuffle on the columns
        -noise (default 0%) (0-1)      -Amount of noise to add to final output
        -featnoise (default 0%) (0-1)   -Percentage of uncorrelated features to generate
        -vectnoise (default 0%) (0-1)  -Percentage of uncorrelated vectors to generate
    ____________________________________    
    
    **Cluster Evolution Options** (IN PROGRESS)
        -evolve (default false) (true, false) -Turn on cluster evolution
        -evint (default 250) -interval to change clusters on
        -evtype (default random) -evolution type (random, *shift - *NOT IMPLEMENTED
    ____________________________________

```****************************************'''
from multiprocessing import Process
from MultiRun import *
import glob
from copy import deepcopy
from itertools import islice


'''************** AUTHOR NICK *************'''

'''
    Run a dimension test, varying the significant dimensions from 50 to 1000
'''
#@numba.jit(nopython=True)
def dimensionTest(argsDict, foName):
    results = ''
    argsDict['featnoise'] = [0.00]
    argsDict['vectors'] = [500]
    argsDict['param']=['dim']
    multirun = int(argsDict['multirun'][0])
    
    if not os.path.exists('./' + foName + '/'):
        os.mkdir('./' + foName + '/')
    
    #Jump in 5's until 50
    for i in range(1,11):
        argsDict['dim'] = [i * 5]
        runMultiRun(argsDict, foName + '/' + foName + str(i), foName + str(i), 'dim='+str(argsDict['dim'][0]))
        results = aggResults(argsDict, foName, results, i)
        
    outfile = file('./' + foName + '/RESULTS_DIMTEST.csv', 'w')
    outfile.write(results)
    outfile.close()
    
    #Jump in 50's until 1000
    for i in range(1, 21):
        argsDict['dim'] = [i * 50]
        runMultiRun(argsDict, foName + '/' + foName + str(i+10), foName + str(i+10), 'dim='+str(argsDict['dim'][0]))
        results = aggResults(argsDict, foName, results, i+10)
    
    outfile = file('./' + foName + '/RESULTS_DIMTEST.csv', 'w')
    outfile.write(results)
    outfile.close()
    
    #Jump in 500's until 2500
    for i in range(3, 6):
        argsDict['dim'] = [i * 500]
        runMultiRun(argsDict, foName + '/' + foName + str(i+30), foName + str(i+30), 'dim='+str(argsDict['dim'][0]))
        results = aggResults(argsDict, foName, results, i+30)
    
    outfile = file('./' + foName + '/RESULTS_DIMTEST.csv', 'w')
    outfile.write(results)
    outfile.close()
    return

'''
    Run an overlap test, varying the cluster distance from .02 to 1
'''
def overlapTest(argsDict, foName):
    argsDict['clusters'] = [2]
    argsDict['csigma'] = [.05]
    argsDict['corg'] = ['bi']
    argsDict['param']=['cdist']
    results = ''
    multirun = int(argsDict['multirun'][0])
    if not os.path.exists('./' + foName + '/'):
        os.mkdir('./' + foName + '/')
    
    for i in range(0, 25):
        argsDict['cdist'] = [.02 * (i + 1)]
        runMultiRun(argsDict, foName + '/' + foName + str(i), foName + str(i), 'cdist='+str(argsDict['cdist'][0]))
        results = aggResults(argsDict, foName, results, i)
        
    outfile = file('./' + foName + '/RESULTS_OVERLAP.csv', 'w')
    outfile.write(results)
    outfile.close()
        
    for i in range(0, 5):
        argsDict['cdist'] = [.5+(.1 * (i + 1))]
        runMultiRun(argsDict, foName + '/' + foName + str(i), foName + str(i), 'cdist='+str(argsDict['cdist'][0]))
        results = aggResults(argsDict, foName, results, i)

    outfile = file('./' + foName + '/RESULTS_OVERLAP.csv', 'w')
    outfile.write(results)
    outfile.close()
    return

'''
    Run an variance test, varying the cluster variance from .02 to 2
'''
def varTest(argsDict, foName):
    argsDict['clusters'] = [2]
    argsDict['param']=['csigma']
    results = ''
    multirun = int(argsDict['multirun'][0])
    if not os.path.exists('./' + foName + '/'):
        os.mkdir('./' + foName + '/')
    
    for i in range(0, 20):
        argsDict['csigma'] = [.5 * (i + 1)]
        runMultiRun(argsDict, foName + '/' + foName + str(i), foName + str(i), 'csigma='+str(argsDict['csigma'][0]))
        results = aggResults(argsDict, foName, results, i)

    outfile = file('./' + foName + '/RESULTS_VARIANCE.csv', 'w')
    outfile.write(results)
    outfile.close()
    return



'''
    Run a column noise test, varying the noisy features from 0% to 100% of total columns
'''
def colNoiseTest(argsDict, foName):
    results = ''
    argsDict['vectors'] = [500]
    argsDict['dim'] = [500]
    argsDict['param']=['featnoise']
    multirun = int(argsDict['multirun'][0])
    
    if not os.path.exists('./' + foName + '/'):
        os.mkdir('./' + foName + '/')
    
    #Jump in .2's starting at 0 until .20
    for i in range(0,11):
        argsDict['featnoise'] = [double(i*2)/100.0]
        runMultiRun(argsDict, foName + '/' + foName + str(i), foName + str(i), 'featnoise='+str(argsDict['featnoise'][0]))
        results = aggResults(argsDict, foName, results, i)

    outfile = file('./' + foName + '/RESULTS_FEATNOISE.csv', 'w')
    outfile.write(results)
    outfile.close()
    
    #Jump in .5's starting at .25 until 1.00
    for i in range(5, 21):
        argsDict['featnoise'] = [double(i * 5)/100.0]
        runMultiRun(argsDict, foName + '/' + foName + str(i+10), foName + str(i+10), 'featnoise='+str(argsDict['featnoise'][0]))
        results = aggResults(argsDict, foName, results, i+10)
    
    outfile = file('./' + foName + '/RESULTS_FEATNOISE.csv', 'w')
    outfile.write(results)
    outfile.close()
    return


'''
    Run a vector noise test, varying the noisy vectors from 0% to 100% of total vectors
'''
def vectNoiseTest(argsDict, foName):
    results = ''
    argsDict['vectors'] = [500]
    argsDict['dim'] = [500]
    argsDict['param']=['vectnoise']
    multirun = int(argsDict['multirun'][0])
    
    if not os.path.exists('./' + foName + '/'):
        os.mkdir('./' + foName + '/')
    
    #Jump in .2's starting at 0 until .20
    for i in range(0,11):
        argsDict['vectnoise'] = [double(i*2)/100.0]
        runMultiRun(argsDict, foName + '/' + foName + str(i), foName + str(i), 'vectnoise='+str(argsDict['vectnoise'][0]))
        results = aggResults(argsDict, foName, results, i)

    outfile = file('./' + foName + '/RESULTS_VECTNOISE.csv', 'w')
    outfile.write(results)
    outfile.close()
    
    #Jump in .5's starting at .25 until 1.00
    for i in range(5, 21):
        argsDict['vectnoise'] = [double(i * 5)/100.0]
        runMultiRun(argsDict, foName + '/' + foName + str(i+10), foName + str(i+10), 'vectnoise='+str(argsDict['vectnoise'][0]))
        results = aggResults(argsDict, foName, results, i+10)
    
    outfile = file('./' + foName + '/RESULTS_VECTNOISE.csv', 'w')
    outfile.write(results)
    outfile.close()
    return

'''
    Run a random noise test, varying the noise from 0% to 100% of total values (cells)
'''
def noiseTest(argsDict, foName):
    results = ''
    argsDict['vectors'] = [500]
    argsDict['dim'] = [500]
    argsDict['param']=['noise']
    multirun = int(argsDict['multirun'][0])
    
    if not os.path.exists('./' + foName + '/'):
        os.mkdir('./' + foName + '/')
    
    #Jump in .2's starting at 0 until .20
    for i in range(0,11):
        argsDict['noise'] = [double(i*2)/100.0]
        runMultiRun(argsDict, foName + '/' + foName + str(i), foName + str(i), 'noise='+str(argsDict['noise'][0]))
        results = aggResults(argsDict, foName, results, i)

    outfile = file('./' + foName + '/RESULTS_RANDNOISE.csv', 'w')
    outfile.write(results)
    outfile.close()
    
    #Jump in .5's starting at .25 until 1.00
    for i in range(5, 21):
        argsDict['noise'] = [double(i * 5)/100.0]
        runMultiRun(argsDict, foName + '/' + foName + str(i+10), foName + str(i+10), 'noise='+str(argsDict['noise'][0]))
        results = aggResults(argsDict, foName, results, i+10)
    
    outfile = file('./' + foName + '/RESULTS_RANDNOISE.csv', 'w')
    outfile.write(results)
    outfile.close()
   
    
    return



'''
    Run a vector test, increasing the number of vectors from 5 to 2500
'''
def vectorTest(argsDict, foName):
    results = ''
    argsDict['dummyCols'] = [0]
    argsDict['dim'] = [500]
    multirun = int(argsDict['multirun'][0])
    argsDict['param']=['vectors']
    
    if not os.path.exists('./' + foName + '/'):
        os.mkdir('./' + foName + '/')
    
    #Jump in 5's until 50
    for i in range(2,11):
        argsDict['vectors'] = [i * 5]
        runMultiRun(argsDict, foName + '/' + foName + str(i), foName + str(i), 'vect='+str(argsDict['vectors'][0]))
        results = aggResults(argsDict, foName, results, i)

    outfile = file('./' + foName + '/RESULTS_VECTTEST.csv', 'w')
    outfile.write(results)
    outfile.close()
    
    #Jump in 50's until 1000
    for i in range(1, 21):
        argsDict['vectors'] = [i * 50]
        runMultiRun(argsDict, foName + '/' + foName + str(i+10), foName + str(i+10), 'vect='+str(argsDict['vectors'][0]))
        results = aggResults(argsDict, foName, results, i+10)
    
    outfile = file('./' + foName + '/RESULTS_VECTTEST.csv', 'w')
    outfile.write(results)
    outfile.close()
    
    #Jump in 500's until 2500
    for i in range(3, 6):
        argsDict['vectors'] = [i * 500]
        runMultiRun(argsDict, foName + '/' + foName + str(i+30), foName + str(i+30), 'vect='+str(argsDict['vectors'][0]))
        results = aggResults(argsDict, foName, results, i+30)
    
    outfile = file('./' + foName + '/RESULTS_VECTTEST.csv', 'w')
    outfile.write(results)
    outfile.close()
    
    return

'''
    Run a cluster test, increasing the number of clusters from 2 to 100
'''
def clustsTest(argsDict, foName):
    results = ''
    argsDict['vectors'] = [500]
    argsDict['dim'] = [250]
    argsDict['param']=['clusters']
    multirun = int(argsDict['multirun'][0])
    
    if not os.path.exists('./' + foName + '/'):
        os.mkdir('./' + foName + '/')
    
    #Jump in 1's starting at 2 until 10
    for i in range(2,11):
        argsDict['clusters'] = [i]
        runMultiRun(argsDict, foName + '/' + foName + str(i), foName + str(i), 'clusters='+str(argsDict['clusters'][0]))
        results = aggResults(argsDict, foName, results, i)

    outfile = file('./' + foName + '/RESULTS_CLUSTSTEST.csv', 'w')
    outfile.write(results)
    outfile.close()
    
    #Jump in 3's starting at 10 until 40
    for i in range(1, 11):
        argsDict['clusters'] = [(i * 3) + 10]
        runMultiRun(argsDict, foName + '/' + foName + str(i+10), foName + str(i+10), 'clusters='+str(argsDict['clusters'][0]))
        results = aggResults(argsDict, foName, results, i+10)
    
    outfile = file('./' + foName + '/RESULTS_CLUSTSTEST.csv', 'w')
    outfile.write(results)
    outfile.close()
    
    #Jump in 10's until 100
    for i in range(1, 7):
        argsDict['clusters'] = [(i * 10) + 40]
        runMultiRun(argsDict, foName + '/' + foName + str(i+30), foName + str(i+30), 'clusters='+str(argsDict['clusters'][0]))
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
        
        p_list=[]
        if 'overlap' in testType or 'all' in testType:
            p_list.append(Process(target=overlapTest, args=(deepcopy(argsdict), fn + '.overlap')))
        
        if 'vectnoise' in testType or 'all' in testType:
            p_list.append(Process(target=vectNoiseTest, args=(deepcopy(argsdict), fn + '.vectNoise')))
            
        if 'colnoise' in testType or 'all' in testType:
            p_list.append(Process(target=colNoiseTest, args=(deepcopy(argsdict), fn + '.colNoise')))
                   
        if 'dim' in testType or 'all' in testType:
            p_list.append(Process(target=noiseTest, args=(deepcopy(argsdict), fn + '.randNoise')))

        if 'randnoise' in testType or 'all' in testType:
            p_list.append(Process(target=clustsTest, args=(deepcopy(argsdict), fn + '.clusts')))

        if 'clusts' in testType or 'all' in testType:
            p_list.append(Process(target=dimensionTest, args=(deepcopy(argsdict), fn + '.dim')))

        if 'vect' in testType or 'all' in testType:
            p_list.append(Process(target=vectorTest, args=(deepcopy(argsdict), fn + '.vect')))

        if 'var' in testType or 'all' in testType:
            p_list.append(Process(target=varTest, args=(deepcopy(argsdict), fn + '.var')))
            
        #if parallel...
        if(argsdict['multithread'][0]=='true'):
            #TODO: implement max thread spawn
            
            for p in p_list:
                p.start()
            
            for p in p_list:
                p.join ()
                
        else:
            for p in p_list:
                p.start()
                p.join()
            
    else:
        print "Requires [testType] [outputFolder] [Option=<...>]\n\tSee TestSeqs.py for options and information"

        
'''****************************************'''
    
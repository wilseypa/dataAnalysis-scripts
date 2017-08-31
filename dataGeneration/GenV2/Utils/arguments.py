import argparse


class arguments():
    
    def __init__(self):
        #TODO
        return
    
    def defaultArgs(self,  argsDict):
        #Todo: Add Default Arguments:
        ''' GENERATION DEFAULTS '''
        
        if not 'minValue' in argsDict:  #DEFAULT  -.999
            argsDict['minValue'] = [-.999]
        if not 'maxValue' in argsDict:  #DEFAULT .999
            argsDict['maxValue'] = [.999]
        if not 'scaling' in argsDict:  #DEFAULT 'true'
            argsDict['scaling'] = ['true']
            
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
    
    def argumentRun(self):
        #TODO
        parser = argparse.ArgumentParser(description='Data Generator and Test Sequences arguments for the DataGenerator V2 Suite')
        
        #Argument Settings and Default Arguments HERE
        parser.add_argument('--vectors',  '-v', help='Number of vectors to generate',  default=1000)
        parser.add_argument('--clusters', '-c', help='Number of clusters to generate',  default=3)
        parser.add_argument('--dimensions','-d','--features', help='Number of dimensions to generate',  default=1000)
        parser.add_argument('--minValue',  '-mi', help='Minimum value to scale to', default=-.999)
        parser.add_argument('--maxValue',  '-ma', help='Maximum value to scale to', default=.999)
        parser.add_argument('--scaling', '-s',  help='Scaling of values (True/False)',  default=True)
        parser.add_argument('--distribution', '-dist',  '-di',  help='Distribution to select values from',  default='gauss')
        parser.add_argument('--centroidDistance','-cdist', '-cd',  help='Target distance between generated centroids',  default=0.4)
        parser.add_argument('--csigma','-csig',  help='Standard deviation of generated points around centroid',default=0.1)
        parser.add_argument('--ccounts','-cc', help='Determines how to split counts of vectors in each cluster assignment', default='random')
        parser.add_argument('--extension','-ext', help='Set which extension modules to use from the generator',  default='all')
        parser.add_argument('--execute','-exec','-exe',help='Determines what methods to use for testSequences', default='cluster' )
        parser.add_argument('--evolve',  '-ev', help='Generate evolving clusters (True/False)', default=False)
        parser.add_argument('--evolveTime', '-et',  help='Vectors before an evolution occurs', default=50)
        parser.add_argument('--evolveType', '-ety', help='How to evolve the clusters when an evolution occurs', default='random')
        parser.add_argument('--chartsType', '-charts', '-ct', help='Format to generate charts into', default='pdf')
        parser.add_argument('--chartsOutput','-output','-co', help='Define what charts to output',  default='all')
        parser.add_argument('--param','--parameter',  '-p',  help='Additonal parameter to list on output', default='vectors')
        parser.add_argument('--multithread','-mt',help='Settings for testSequence multithreading', default=True)
        parser.add_argument('--maxThreads',  '-mth', help='Maximum threads to use for testSequence multithreading',  default=2)
        parser.add_argument('--multirun', '-mr',  help='Number of times to multirun (regenerate) for given parameters',  default=5)
        parser.add_argument('--batches','-b', help='Number of batches to run',  default=2)
        parser.add_argument('--rshuf',  '-rs',  help='Shuffle the rows (True/False)',default=True)
        parser.add_argument('--cshuf', '-cs', help='Shuffle the columns (True/False)', default=True)
        parser.add_argument('--featureNoise', '-fn',  help='Percentage of feature noise to generate', default=0.00)
        parser.add_argument('--vectorNoise', '--vectNoise', '-vn',  help='Percentage of vector noise to generate',  default=0.00)
        parser.add_argument('--randomNoise', '--noise',  '-rn', help='Percentage of random noise to generate',  default=0.00)
        
        ##TODO: Still need to add additional RPHash parameters and complete more testing on the above parameters
        parser.add_argument('--RPparallel', '-rpp',  help='Run RPHash in parallel (True/False)',  default=True)
        parser.add_argument('--RPdecodertype', '-rpd',  help='Run RPHash with specified decoder',  default='adaptive')
        parser.add_argument('--RPnumprojections', '-rpn',  help='Run RPHash with specified number of projections', default=1)
        parser.add_argument('--RPnumblur', '-rpb',  help='Run RPHash with specified blur',  default=0)
        parser.add_argument('--RPruns',  '-rpr',  help='Run RPHash with specified runs',  default=1)
        parser.add_argument('--RPclustermethod',  '-rpc',  help='Run RPHash with specified cluster method', default='adaptive')
        parser.add_argument('--RPofflineclusterer',  '-rpo',  help='Run RPHash with specified offline clusterer', default='none')
        parser.add_argument('--RPdimparameter',  '-rpdim',  help='Run RPHash with specified dim parameter', default=24)
        parser.add_argument('--RPprojection',  '-rpproj',  help='Run RPHash with specified projection method', default='dbf')
        
        
        
        
        
        args = parser.parse_args()
        args = vars(args)
        args = self.defaultArgs(args)
        print args
        print "Test"
        return args



        
        
        
        
        
        

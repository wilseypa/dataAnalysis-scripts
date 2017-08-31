''' 
    Label Generator:
        -Outputs centroid labels based number of clusters
            and the cluster counts
        -Number of clusters limits min/max ID [0 to N-1]
        -Cluster counts determine how the total number of 
            vectors is binned between the clusters
            
'''

import numpy as np
from copy import deepcopy


class LabelGenerator():
    argDict = None
    '''
        Initialize the Label Generator; store the argument
            dictionary and generated labels locally
    '''
    def __init__(self, argDict):
        self.argDict = deepcopy(argDict)
        self.labels = []
    
        return
    
    '''
        Generates cluster ids from 1 to # of clusters
    '''
    def idClusters(self):        
        retIds = []
        clusters = int(self.argDict["clusters"])
        vectors = int(self.argDict["vectors"])
        ccounts = self.argDict["ccounts"]
        
        if ccounts == 'equal':
            for i in range(0, int(clusters)):
                z = np.array([i for t in range(0, vectors/clusters)])
                
                if (retIds == []):
                    retIds = z
                else:
                    retIds = np.append(retIds, z);   
                
        elif ccounts == 'separated':
            #TODO: 
            print "Not Implemented" 
        else: #random or nothing was entered
            zc = (np.random.randn(clusters) * (.1*(vectors/clusters))) + (vectors/clusters)
            tot = 0
            for i in range(0,int(clusters) - 1):
                z = np.array([i for t in range(0, int(zc[i])) ])
                
                tot = tot + int(zc[i])
                
                if (retIds == []):
                    retIds = z
                else:
                    retIds = np.hstack((retIds, z)); 
            
            z = np.array([int(clusters-1) for t in range(0, vectors - tot)])
            if (retIds == []):
                retIds = z
            else:
                retIds = np.hstack((retIds, z)); 
        
        return retIds

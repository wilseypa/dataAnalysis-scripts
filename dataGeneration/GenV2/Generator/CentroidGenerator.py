''' 
    Centroid Generator:
            
'''

import numpy as np
from copy import deepcopy


class CentroidGenerator():
    argDict = None
    labels = []
    
    '''
        Initialize the Label Generator; store the argument
            dictionary and generated labels locally
    '''
    def __init__(self, argDict,  labels):
        self.argDict = deepcopy(argDict)
        self.labels = labels
    
        return
    
    '''
    Generates centroids for clusters generation mean
        TODO: Generate nearby clusters (bi, tri, quad, none)
    '''
    def genCentroids(self):
        
        minValue = float(self.argDict["minValue"])
        maxValue = float(self.argDict["maxValue"])
        clusters = int(self.argDict["clusters"])
        dim = int(self.argDict["dimensions"])
        #TODO - 'nearby' clustering for close neighbor
        zf = []
        cOrg = self.argDict["ccounts"]
        scalePerc = float(self.argDict['centroidDistance'])


        if cOrg == 'random':
            zf = np.random.uniform(minValue, maxValue, clusters)#[clusters,  dim])
        if cOrg == 'bi':
            for i in range(0,clusters/2):
                z = np.random.uniform(minValue,maxValue,1)
                z1 = np.random.uniform((1-scalePerc)*z,(1+scalePerc)*z,1)
                z = np.vstack((z,z1))
                
                if(zf == []):
                    zf = z
                else:
                    zf = np.vstack((zf,z))
                    
            if(clusters%2 > 0):
                z = np.random.uniform(minValue,maxValue,1)
                if(zf == []):
                    zf = z
                else:
                    zf = np.append(zf,z,1)
                
        if cOrg == 'tri':
            for i in range(0,clusters/3):
                z = np.random.uniform(minValue,maxValue,1)
                z1 = np.random.uniform((1-scalePerc)*z,(1+scalePerc)*z,1)
                z2 = np.random.uniform((1-scalePerc)*z,(1+scalePerc)*z,1)
                z1 = np.append(z1,z2,1)
                z = np.append(z,z1,1)
                if(zf == []):
                    zf = z
                else:
                    zf = np.append(zf,z,1)
                
            if(clusters%3 == 1):
                np.random.uniform(minValue,maxValue,1)
            if(clusters%3 == 2):
                z = np.random.uniform(minValue,maxValue,1)
                z1 = np.random.uniform((1-scalePerc)*z,(1+scalePerc)*z,1)
                z = np.append(z,z1,1)
                
                if(zf == []):
                    zf = z
                else:
                    zf = np.append(zf,z,1)
            
        if cOrg == 'quad':
            for i in range(0,clusters/4):
                z = np.random.uniform(minValue,maxValue,1)
                z1 = np.random.uniform((1-scalePerc)*z,(1+scalePerc)*z,1)
                z2 = np.random.uniform((1-scalePerc)*z,(1+scalePerc)*z,1)
                z3 = np.random.uniform((1-scalePerc)*z,(1+scalePerc)*z,1)
                z2 = np.append(z2,z3,1)
                z1 = np.append(z1,z2,1)
                z = np.append(z,z1,1)
                if(zf == []):
                    zf = z
                else:
                    zf = np.append(zf,z,1)
                    
            if(clusters%4 == 1):
                np.random.uniform(minValue,maxValue,1)
            if(clusters%4 == 2):
                z = np.random.uniform(minValue,maxValue,1)
                z1 = np.random.uniform((1-scalePerc)*z,(1+scalePerc)*z,1)
                z = np.append(z,z1,1)
                if(zf == []):
                    zf = z
                else:
                    zf = np.append(zf,z,1)
            if(clusters%4 == 3):
                z = np.random.uniform(minValue,maxValue,1)
                z1 = np.random.uniform((1-scalePerc)*z,(1+scalePerc)*z,1)
                z2 = np.random.uniform((1-scalePerc)*z,(1+scalePerc)*z,1)
                z1 = np.append(z1,z2,1)
                z = np.append(z,z1,1)
                if(zf == []):
                    zf = z
                else:
                    zf = np.append(zf,z,1)

        
        return zf

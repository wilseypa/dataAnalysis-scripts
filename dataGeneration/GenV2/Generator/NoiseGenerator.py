''' 
    Noise Generator:
            
'''

import numpy as np
from copy import deepcopy
from math import ceil, floor



class NoiseGenerator():
    argDict = None
    targetArray = []
    '''
        Initialize the Noise Generator; store the argument
            dictionary and generated labels locally
    '''
    def __init__(self, argDict):
        self.argDict = deepcopy(argDict)
        
        return
    
    def genNoiseComponents(self, data, labels):
        data = self.genVectorNoise(data)
        data = self.genFeatureNoise(data)
        data = self.genRandomNoise(data)
        data, labels = self.shuffleRows(data, labels)
        data = self.shuffleCols(data)
        return data, labels
    
    
    def genVectorNoise(self, data):
        if(self.targetArray == []):
            targetPoints = int(float(self.argDict["vectorNoise"])* float(len(data)))
            self.targetArray = np.random.choice(len(data), targetPoints, replace=False)
            
        for i in xrange(len(self.targetArray)):
            data[self.targetArray[i]] = np.random.uniform(float(self.argDict["minValue"]),float(self.argDict["maxValue"]));
        return data
    
    def genFeatureNoise(self, data):
        dim = int(self.argDict['dimensions'])
        dummyCols = floor(float(self.argDict['featureNoise'])* dim)
        if(dummyCols == dim):
            dummyCols = dummyCols - 1
    
        vectors = len(data)
        z = np.random.uniform(0,0,[vectors, int(dummyCols)]);
        data = np.append(data, z, 1)
        
        return data
    
    
    def genRandomNoise (self, data):
        targetPoints = int(float(self.argDict["randomNoise"]) * len(data))
    
        targetArray = np.random.choice(range(len(data)), targetPoints, replace=False)
    
        for i in xrange(len(targetArray)):
            data[targetArray[i]] = np.random.uniform(float(self.argDict["minValue"]),float(self.argDict["maxValue"]));
        
        return data
    
    def shuffleRows(self,data, labels):
        if(self.argDict["cshuf"] == True):
            idsout = np.column_stack((data, labels))
            np.random.shuffle(idsout)
            data = idsout[:,:-1]
            labels = idsout[:,-1:]
        return data, labels
    
    
    def shuffleCols(self,data):
        if(self.argDict["rshuf"] == True):
            data = np.transpose(data)
            np.random.shuffle(data)
            data = np.transpose(data)
        
        return data
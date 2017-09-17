import numpy as np


class ObjectGenerator():
    argDict = []
    labels = []
    centroids = []
    
    def __init__(self,argDict,labels,  centroids, centroidGenerator):
        self.argDict = argDict
        self.labels = labels
        self.centroids = centroids
        self.centroidGenerator = centroidGenerator
        return;
        
    def getCents(self):
        return self.centroidGenerator.genCentroids()

    def scaleAssurance(self,data):
        minValue = self.argDict["minValue"]
        maxValue = self.argDict["maxValue"]
        mins = np.min(z)
        maxs = np.max(z)
    
        rng = maxs - mins
        #Normalize
        z = maxValue - (((maxValue - minValue) * (maxs - z)) / rng)

        return z
        
        
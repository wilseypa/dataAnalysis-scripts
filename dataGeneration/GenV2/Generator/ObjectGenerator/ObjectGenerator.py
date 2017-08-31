
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

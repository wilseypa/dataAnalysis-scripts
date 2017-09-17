from ObjectGenerator import *
import random
import math

class TwoDObjectGenerator(ObjectGenerator):
    def testData(self):
        return 1
    
    def generate(self):
        self.centroids = np.column_stack((self.getCents(), self.getCents()))
        print self.centroids
        data = self.genCircles()
        
        return data,  self.centroids

    def genCircles(self):
        clusters = int(self.argDict["clusters"])
        print "test: " + str(len(self.labels))
        
        rx = []
        ry = []
        ret = []
        
        for i in range(0,len(self.labels)):            
            alpha = 2 * math.pi * random.random()
            
            radius = 0.1
            
            r = radius #* (random.random())
            x = r*math.cos(alpha) + self.centroids[self.labels[i],0]
            y = r*math.sin(alpha) + self.centroids[self.labels[i],1]
            
            
            if rx == []:
                rx = np.copy(np.array(x))
                ry = np.copy(np.array(y))
            else:
                rx = np.vstack((rx, np.array(x)))
                ry = np.vstack((ry,np.array(y)))
                
        ret = np.append(rx,ry,1)
        print ret.shape
        #print ret
        return ret

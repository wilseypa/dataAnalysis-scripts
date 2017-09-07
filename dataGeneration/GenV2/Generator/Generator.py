from LabelGenerator import *
from ObjectGenerator import OneDObjectGenerator
from CentroidGenerator import *
from NoiseGenerator import *
from copy import deepcopy

class Generator():
    
    '''    A simple generator class for demonstration of the new refactoring of the Generator '''
    
    def __init__(self, argDict):
        self.test = True
        self.argDict = deepcopy(argDict)
        
        return
    
    
    def generateData(self):
        #Steps to generating data:
        #    1. Generate data labels (LabelGenerator.py)
        #        # of Vectors, # of Clusters, %VectorNoise, Cluster Counts
        #   1.5 = generate the centroids, dummy!
        #    2. While data is left to generate... (more columns):
        #        a. Pick a new object (1D, 2D, 3D, ND, FeatureNoise)
        #        b. Generate tht_e new object using the labeled data
        #        c. Append the data columns to the complete data set
        #    3. Add random noise to data
        #    4. Output data to files (MAT, LBL, CSV, ETC.)
        #    5. Basic plots of data to output
        lg = LabelGenerator(self.argDict)
        lbl = lg.idClusters()
        a = len(lbl)
        
        object = 'none'
        
        # Keep generating centroids during an evolution?
        cg = CentroidGenerator(self.argDict, lbl)
        
        data = []
        t_data = []
        cents = []
        t_cents = []
        
            
        while (a > 0):
            if object == '1D':
                og = OneDObjectGenerator.OneDObjectGenerator(self.argDict,  lbl,  t_cents,  cg)
                a = a-1
            elif object == '2D':
                og = TwoDObjectGenerator.TwoDObjectGenerator(self.argDict,  lbl,  t_cents,  cg)
                a = a-2
            elif object == '3D':
                og = ThreeDObjectGenerator.ThreeDObjectGenerator(self.argDict,  lbl,  t_cents,  cg)
                a = a-3
            elif object == 'ND':
                og = NdObjectGenerator.NdObjectGenerator(self.argDict,  lbl,  t_cents,  cg)
                # TODO: a = a-
            else: 
                og = OneDObjectGenerator.OneDObjectGenerator(self.argDict,  lbl, t_cents,  cg)
                a = a-1
                
            
                
            t_data, t_cents = og.generate()   
            
            if(data == []):
                data = t_data
                cents = t_cents
                #centsF = cents
            else:
                data = np.append(data, t_data, 1)
                cents = np.column_stack((cents,  t_cents))
                #centsF = np.column_stack((centsF, cents))
        
        
        ng = NoiseGenerator(self.argDict)
        ng.genNoiseComponents(data, lbl)
        
        print data
        print cents
        return data,  cents,  lbl;
    
    
if __name__ == "__main__":
    # Read and parse our argument dictionary (KVP)
    argDict = arguments.arguments()
    argDict = argDict.argumentRun()

    # Create a generator interface 
    gen = Generator.Generator(argDict)

    # Generate the data (x MultiRun)
    gen.generateData()

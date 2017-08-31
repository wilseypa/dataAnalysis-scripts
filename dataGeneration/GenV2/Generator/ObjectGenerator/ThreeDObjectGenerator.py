from ObjectGenerator import *

class ThreeDObjectGenerator(ObjectGenerator):
    
    
    def __init__(self,argDict):
        super().__init__(argDict)
        return


    def genRawColumn(argsDict, clusters, ids, dist, vectors, minValue, maxValue, csigma):
    
        cents = genCentroids(argsDict, clusters, minValue, maxValue)
        zf = []
        bc = np.bincount(ids)    
        
        if dist == "gauss" or dist == "normal" or dist == "norm" or dist == "gaussian":
            for r in range(0, clusters):
                z = np.random.randn(bc[r], 1)
                z = z * csigma
                z = z + cents[r]
                if(zf == []):
                    zf=np.copy(z)
                else:
                    zf = np.vstack((zf, z))
                
        elif dist == "binomial" or dist == "binom":
            # n * p = mean; mean/n = p
            n = 1000
            if "n" in argsDict:
                 n = float(argsDict["n"][0])
            for r in range(0, clusters):
                z = z * csigma
                z = np.random.binomial(n,cents[r]/n,[bc[r], 1])
                if(zf == []):
                    zf = z
                else:
                    zf = np.append(z,zf,axis=0)

        elif dist == "exponential" or dist == "exp":
            # mean = l^-1 = (1/l) = B
            for r in range(0, clusters): 
                l = 1/cents[r - 1]
                z = np.random.exponential(l,[bc[r], 1])
                z = z*csigma
                if(zf == []):
                    zf = z
                else:
                    zf = np.append(z,zf,axis=0)

        elif dist == "uniform" or dist == "uni":
            for r in range(0, clusters):
                z = np.random.uniform(cents[r] -1, cents[r] + 1, [bc[r], 1])
                z = z*csigma
                if(zf == []):
                    zf = z
                else:
                    zf = np.append(z,zf,axis=0)

        return zf, cents

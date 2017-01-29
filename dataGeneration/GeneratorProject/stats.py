

import numpy as np




def calcPurity(ids, input, mapping):
    bcid = np.bincount(ids) 
    bcin = np.bincount(input[:,0])
    count = 0
    
    for i in xrange(len(input)):
        if int(input[i]) < len(mapping):
            if int(ids[i]) == int(mapping[int(input[i])]):
                count += 1
    
    purity = count/float(len(input))
    print "\tRun Purity: " + str(purity)
    if purity == 0.0:
        print bcid
        print bcin
    
    return purity




def calcARI(ids, input, mapping):
    
    
    
    return





def calcRI(ids, input, mapping):
    
    return
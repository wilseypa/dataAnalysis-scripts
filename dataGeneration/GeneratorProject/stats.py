import numpy as np
from sklearn import metrics

'''************** AUTHOR NICK *************'''
def calcCentroidMetrics(ids,input,mapping):
    ids = ids.flatten()
    input = input.flatten()
    ari = metrics.adjusted_rand_score(ids,input)
    nmi = metrics.normalized_mutual_info_score(ids,input)
    ami = metrics.adjusted_mutual_info_score(ids,input)
    homogeneity = metrics.homogeneity_score(ids,input)
    completeness = metrics.completeness_score(ids,input)
    vscore = metrics.v_measure_score(ids,input)
    fmi = metrics.fowlkes_mallows_score(ids,input)
    
    return ari,nmi,ami,homogeneity,completeness,vscore,fmi
    

def calcPurity(ids, input, mapping):
    bcid = np.bincount(ids) 
    bcin = np.bincount(input[:,0])
    count = 0
    
    for i in xrange(len(input)):
        if int(input[i]) < len(mapping):
            if int(ids[i]) == int(mapping[int(input[i])]):
                count += 1
    
    purity = count/float(len(input))
    
    return purity





'''****************************************'''
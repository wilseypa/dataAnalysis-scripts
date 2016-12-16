import sys
'''

things to preserve
1. column variance
2. cluster bias (higher sample bias for larger clusters)
3. datatype, binary vs floating point

author: lee
'''

OUTPUT_MAT_ONLY = False
def readNextVecUpdateModel(line,fpdata,counts,MEANS,VARIANCES):
    '''
        read from csv one row at a time, update model
        this will support streaming and should have
        very low memory overhead
    '''
    cols = line.split(',')
    clusterID = int(cols[-1][:-1])
    vec = []
    if len(fpdata)==0:
        fpdata = [False for i in xrange((len(cols)-1))]
    for colnum in xrange(len(cols)-1):
        #check if data is discrete, this can change for new vectors
        #   eg 0 is discrete, but could just have been empty in the
        #   first set of vectors
        if cols[colnum].count('.')>0 or cols[colnum].count('e')>0:
            fpdata[colnum] = True

        # parse using either discrete or integer parser
        if fpdata[colnum]:
            vec.append(float(cols[colnum]))
        else:
            vec.append(int(cols[colnum]))

    #update cluster model if cluster id exists, create new cluster model otherwise
    if counts.has_key(clusterID):
        cnt_r,x_r,var_r = mergecent(MEANS[clusterID],VARIANCES[clusterID],counts[clusterID],vec,[0]*len(vec),1)
        counts[clusterID] = cnt_r
        MEANS[clusterID] = x_r
        VARIANCES[clusterID] = var_r
    else:
        counts[clusterID] = 1
        MEANS[clusterID] = vec
        VARIANCES[clusterID] = [0]*len(vec)


    return fpdata,counts,MEANS,VARIANCES


def mergecent(x_1,var_1,cnt_1,x_2,var_2,cnt_2):
    '''
        this is our old friend, weighted mean and variance combiner
    '''
    cnt_r = cnt_1+cnt_2;
    x_r = [0.0]*len(x_1)
    var_r = [0.0]*len(x_1)
    for i in xrange(len(x_1)):
        x_r[i] = (cnt_1*x_1[i] + cnt_2*x_2[i] ) / float(cnt_r)
        var_r[i] +=  cnt_1*( (x_r[i]-x_1[i])**2 +var_1[i])+  cnt_2*( (x_r[i]-x_2[i])**2 + var_2[i])
        var_r[i] = var_r[i]/float(cnt_r)
    return cnt_r,x_r,var_r

def createModel(infile):
    '''
        create a model for the input data
    '''
    VARIANCES = {}
    MEANS = {}
    counts = {}
    fpdata = []
    line = infile.readline()
    while not line == '':
        fpdata,counts,MEANS,VARIANCES = readNextVecUpdateModel(line,fpdata,counts,MEANS,VARIANCES)
        line = infile.readline()

    return fpdata,counts,MEANS,VARIANCES

def genfpvecdata(i,mean,variance):
    '''
        generate gaussian data for a continuous column
    '''
    return gauss(mean[i],variance[i])


def gendiscretevecdata(i,mean,variance):
    '''
        generate data for a discrete column
    '''
    r = random()
    if r < mean[i]: return 1
    if r > mean[i]: return 0
    #flip a coin if right on the mean
    return random()+.5


from random import *
def generateNextVec(total,fpdata,counts,MEANS,VARIANCES):
    '''
        generate the next vector based on the input model
    '''
    randomclurange = randrange(total)
    rangecounter = 0

    #select a random cluster based on the cluster counts distribution
    clusterID = 0
    for key in counts.keys():
        rangecounter = rangecounter + counts[key]
        if randomclurange < rangecounter:
            clusterID = key
            break

    vec = []
    for i in range(len(MEANS[clusterID])):

        if fpdata[i]:
            vec.append(genfpvecdata(i,MEANS[clusterID],VARIANCES[clusterID]))
        else:
            vec.append(gendiscretevecdata(i,MEANS[clusterID],VARIANCES[clusterID]))
    return clusterID,vec


def gendata(infile,outfile,n):
    '''
        read in data, generate model, write out similar data based on model
    '''
    fpdata,counts,MEANS,VARIANCES = createModel(infile)
    total = 0
    for key in counts.keys():
        total += counts[key]
    if OUTPUT_MAT_ONLY:
        outfile.write(str(n)+'\n'+str(len(fpdata))+'\n')
        for i in xrange(n):
            clusterid, vec = generateNextVec(total,fpdata,counts,MEANS,VARIANCES)
            outfile.write(str(vec)[1:-1].replace(',','\n').replace(' ',''))
    else:
        for i in xrange(n):
            clusterid, vec= generateNextVec(total,fpdata,counts,MEANS,VARIANCES)
            outfile.write(str(vec)[1:-1]+','+str(clusterid) +'\n')


'''
    shortcomings:
    assumes all axis are gaussian if they contain floating point numbers
    and uniform if they are discrete 0/1
    the basic steps are
    1. read data from file
    2. compute
      a. means for each cluster,
      b. counts for each cluster,
      c. variances for each cluster
      d. decide if data is discrete or continuous
    3. generate data
      a. pick a cluster based on the counts distributions (ie generate data for larger clusters more often than data for smaller clusters)
      b. if data is discrete use the uniform generator based on cluster's mean, to output either 0 or 1
      c. if data is continuous use the gaussian generator using mean and variance to generate data
    4. write data to a file (default is labelled csv)
'''
if len(sys.argv)>3:
    infile = file(sys.argv[1],'r')
    outfile = file(sys.argv[2],'w')
    size = int(sys.argv[3])
    OUTPUT_MAT_ONLY = len(sys.argv)>4 and bool(sys.argv[4])
    gendata(infile,outfile,size)
    infile.close()
    outfile.close()


else:
    print "Requires InputFile Outputfile size [true]"

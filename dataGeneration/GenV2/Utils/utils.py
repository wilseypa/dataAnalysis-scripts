import datetime
import csv
import numpy as np

class utils():
    
    def __init__(self, argDict):
        self.argDict = argDict
        
    def outputConfiguration(self,  fPathRaw, cRaw):
        outfile = file(fPathRaw + '_CFG', 'w')
        outfile.write('******Raw Command (COPY THIS)******')
        outfile.write('\n\tpython ' + cRaw + '\n\n')

        outfile.write('******CONFIGURATION FOR GENERATION: ' + fPathRaw + ' | ')
        outfile.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +'******\n')

        outfile.write('\n' + str(self.argDict).replace(',','\n').replace('{',' ').replace('}','') + '\n')
        return
        
    def readDataFromFile(self,  rawFileName, type):
        result = csv.reader(open(rawFileName,"rb"),delimiter=',')
        result = np.array(list(result)).astype('float')
        return result.astype(type)

    def outputRawData(self,  filepath,  data):
        vectors = int(self.argDict["vectors"])
        dimensions = int(self.argDict["dimensions"])
        
        outfile = file(filepath + '_RAW','w')
        outfile.write(str(vectors)+'\n'+str(dimensions)+'\n')
        for i in xrange(vectors):
            for dim in xrange(dimensions):
                outfile.write(str(data[i,dim]))
                if i != vectors-1 or dim!=dimensions-1:
                    outfile.write('\n')
        outfile.close()
        
    def outputLabels(self,  filepath, labels):
        outfile = file(filepath + '_LBLONLY.csv','w')
        outfile.write(str(len(labels))+'\n1\n')
        for i in xrange(len(labels)):
            outfile.write(str(labels[i]) + "\n")
        outfile.close()
        
    def outputCents(self,  filepath,  cents):
        outfile = file(filepath + '_CENTS.csv','w')
        dimensions = int(self.argDict["dimensions"])
        for i in xrange(len(cents)):
            if(dimensions == 1):
                outfile.write(str(cents[i]) + '\n')
            else:
                for dim in xrange(dimensions):
                    outfile.write(str(cents[i,dim]) + ',')
                outfile.write('\n')
        outfile.close()

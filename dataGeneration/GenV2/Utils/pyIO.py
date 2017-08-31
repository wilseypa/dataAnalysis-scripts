import datetime
import csv

class pyIO():
    def __init__(self,argDict):
        self.argDict = argDict


    def readCSVData(self, inFile, type):
        result = csv.reader(open(inFile,"rb"),delimiter=',')
        result = np.array(list(result)).astype('float')
        return result.astype(type)
    
    
    def writeMATData(self, data, outFile):
        outfile = file(outFile,'w')
        outfile.write(str(len(data))+'\n'+str(data)+'\n')
        for i in xrange(len(data)):
            for dim in xrange(data):
                outfile.write(str(data[i,dim]))
                if i != len(z)-1 or dim!=p-1:
                    outfile.write('\n')
        outfile.close()
    
    
    def writeCSVData(self, data, outFile):
        outfile = file(outFile,'w')
        for i in xrange(len(data)):
            if(self.argsDict.dimensions == 1):
                outfile.write(str(data[i]) + '\n')
            else:
                for dim in xrange(dimensions):
                    outfile.write(str(data[i,dim]) + '\n')
        outfile.close()
        
    
    def outputConfiguration(self,fPathRaw, argsDict, cRaw):
        outfile = file(fPathRaw + '_CFG', 'w')
        outfile.write('******Raw Command (COPY THIS)******')
        outfile.write('\n\tpython ' + cRaw + '\n\n')
    
        outfile.write('******CONFIGURATION FOR GENERATION: ' + fPathRaw + ' | ')
        outfile.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +'******\n')
    
        outfile.write('\n' + str(argsDict).replace(',','\n').replace('{',' ').replace('}','') + '\n')
    
        return
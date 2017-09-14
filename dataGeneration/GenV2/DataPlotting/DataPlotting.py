import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import inspect
import numpy as np
from math import ceil
from copy import deepcopy

class DataPlotting():
    ''' A simple class for plotting the input data '''
    argDict = None
    
    def generateTilePlot(self, data):
        d = int(self.argDict["dimensions"])
        columns = 5
        rows = int(ceil(d/(2*columns)))


        plt.figure(1)
        data = np.transpose(data)
        for n in range(0,rows):
            for m in range(0,columns):
                if 10*n+2*m < d:
                    x_val = [x for x in data[10*n+2*m]]
                    print x_val
                    y_val = [y for y in data[10*n+2*m+1]]
                    plt.subplot(columns, rows, 5*n+m+1)
                    plt.scatter(x_val, y_val)
                    plt.grid(True, which='both')
        return

    def __init__(self, argDict):
        #TODO
        self.argDict = deepcopy(argDict)

    def test(self):
        print "Reached Test!"
        return
        
    def generatePlots(self, fPathRaw, type):
        #TODO
        plt.figure(1)
        if type == 'pdf' or type == 'all':
            plt.savefig(fPathRaw + '.pdf', bbox_inches='tight')
        if type == 'png' or type == 'all':
            plt.savefig(fPathRaw + '.png', bbox_inches='tight')
        return
    
    def clearPlots(self):
        #TODO
        plt.clf()
        return
    
    def showPlots(self):
        #TODO
        plt.show()
        return
    
    def r3DPlot(self, xTestPts, yTestPts, zTestPts, ids, pos, cents, match):
        #TODO
        x_val = [x for x in xTestPts]
        y_val = [y for y in yTestPts]
        z_val = [z for z in zTestPts]

        fig = plt.figure(1)
        ax = fig.add_subplot(pos, projection='3d')

        markers = ['o', 'x']

        colors = ['r', 'c', 'y', 'g', 'b', 'm', 'k']
        for i in range(0, len(x_val)):
            if (match == {}):
                ax.scatter(x_val[i], y_val[i], z_val[i], c=colors[ids[i] % len(colors)], s=0.5)
            else:
                ax.scatter(x_val[i], y_val[i], z_val[i], marker=markers[match[i]], c=colors[ids[i] % len(colors)],
                           s=0.5)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        return
    
    def simplePlot(self,xTestPts, yTestPts, ids, cents, match):
        #TODO
        self.clearPlots()
        x_val = [x for x in xTestPts]
        y_val = [x for x in yTestPts]

        markers = ['o', 'x']
        colors = ['r', 'c', 'y', 'g', 'b', 'm', 'k']

        plt.figure(1)
        #plt.subplot(221)

        for i in range(0, len(x_val)):
            if (match == {}):
                plt.scatter(x_val[i], y_val[i], c=colors[ids[i] % len(colors)], s=1)
            else:
                plt.scatter(x_val[i], y_val[i], marker=markers[match[i]], c=colors[ids[i] % len(colors)], s=1)

        # minx, maxx = checkPlotBoundaries(x_val, minx, maxx)
        # miny, maxy = checkPlotBoundaries(y_val, miny, maxy)

        # plt.axis([minx,maxx,miny,maxy])

        plt.grid(True, which='both')
        return
    
    def eucPlot(self,testPts,ids,cents, match):
        #TODO
        x_val = []
        markers = ['o', 'x']
        colors = ['r', 'c', 'y', 'g', 'b', 'm', 'k']
        for row in testPts:
            x_val.append([np.linalg.norm(row)])
        plt.figure(1)
        plt.subplot(223)

        for i in range(0, len(x_val)):
            if (match == {}):
                plt.scatter(ids[i], x_val[i], c=colors[ids[i] % len(colors)], s=3)
            else:
                plt.scatter(ids[i], x_val[i], marker=markers[match[i]], c=colors[ids[i] % len(colors)], s=3)

        plt.grid(True, which='both')
        return
    
        

        
        
        
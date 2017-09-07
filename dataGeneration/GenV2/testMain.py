from DataPlotting import *
from Utils import *
from TestSequences import TestSequences
from Generator import Generator

# Sequence of events to generate data, run tests, etc.
#    For now, let's just generate some data and leave the rest for later

# Read and parse our argument dictionary (KVP)
argDict = arguments.arguments()
argDict = argDict.argumentRun()

# Create a generator interface 
gen = Generator.Generator(argDict)

# Generate the data (x MultiRun)
data,  cents,  labels = gen.generateData()

# Run the test sequences (x Batch x MultiRun)
ts = TestSequences.TestSequences(argDict)

# Plot the results (x Batch x MultiRun
dp = DataPlotting.DataPlotting(4)
dp.test()

if (len(data[0]) >= 2):
    dp.simplePlot((x[0] for x in data), (x[1] for x in data), labels, cents, {});
if (len(data[0]) >= 3):
    dp.r3DPlot((x[0] for x in data), (x[1] for x in data), (x[2] for x in data), labels, 222, cents, {});
if (len(data[0]) >= 6):
    dp.r3DPlot((x[3] for x in data), (x[4] for x in data), (x[5] for x in data), labels, 224, cents, {});
dp.eucPlot(data, labels, cents, {})
dp.generatePlots("./", argDict["chartsOutput"])
dp.showPlots()
ut = utils.utils(argDict)
ut.outputCents("./testoutput", cents)
ut.outputRawData("./testoutput", data)
ut.outputLabels("./testoutput", labels)

print "Finished with generation testing"

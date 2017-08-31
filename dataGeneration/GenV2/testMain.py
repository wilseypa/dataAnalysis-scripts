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

ut = utils.utils(argDict)
ut.outputCents("./testoutput", cents)
ut.outputRawData("./testoutput", data)
ut.outputLabels("./testoutput", labels)

print "Finished with generation testing"

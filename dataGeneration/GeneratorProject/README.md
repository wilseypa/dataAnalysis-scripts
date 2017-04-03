![DataGeneratorSystem](Images/DataGeneratorSystem.jpeg?raw=true "System Diagram of Data Generator and Testing")


************** REQUIREMENTS *************** 
	
	-Scikit-Learn for various clustering algorithms and result metrics
	
	-MatPlotLib for distribution plotting
		-http://matplotlib.org/faq/installing_faq.html
                
              1)  git clone git://github.com/matplotlib/matplotlib.git
              2)  cd matplotlib
                  python setup.py install

			OR
			
			  1)  pip install matplotlib
			  
	-Updated RPHash.jar and Labeler.jar in root of GeneratorProject
		(from RPHash repository)
		
	-If using LSHKit, must build from source and copy Tool binaries to <root>/LSHKitBin/...
			  
*************** RUNNING ****************

Standard Data Generator:

	##    python DataGenerator.py testOutput
	##    python DataGenerator.py testOutput [option=value]
	##    python DataGenerator.py testOutput infile=inputFile.txt vectors=100
	
MultiRun with Analysis:

	##    python MultiRun.py 5 1-22-17
	##    python MultiRun.py [Num of Runs] [OutputFolderName] [option=value]
	##    python MultiRun.py 5 1-22-17 vectors=100 clusters=6	
	
	
Test Sequences with Analysis:

	##	python TestSeqs.py overlap overlapTestFiles
	##	python TestSeqs.py [testType] [outputFolder] [option=value]
	##	python TestSeqs.py overlap overlapTestFiles vectors=10000 dim=1000
		
		##    Current Test Labels: 'all', 'vectnoise', 'colnoise', 'randnoise',
		##                         'dim', 'vect', 'clusts', 'var', 'overlap'

***************  NOTES  ****************

    -Data generator for testing algorithms
	-Specifically focused on the LSH algorithms
	    -Significance of LSH operation on the data sets
    -Based off of 'generate-from-labelled-dataset.py'

    -Generates data column by column
	-Significant columns are generated using centroids
	-Non-significant columns are uniformly distributed (Noise)

    -Outputs generated data to folder
	    -Raw data (no labels)
	    -Labeled data
	    -Graph Output (Pdf/Png)
	    -Configuration output


*************** OPTIONS ****************

        **General Options**
        -exec (default all)    -Determine what programs to use for analysis
                                'all' - use RPHash, sklearn, and LSHKit (see req's in readme)
                                'rphash' 
                                'lshkit' 
                                'cluster': rphash + sklearn
                                'LSH': rphash + lshkit
                                'none'
    
        -scaling (default true)     -Toggle scaling of generated data
        -minValue (default -.999)   -Max value of output data
        -maxValue (default .999)    -Min value of output data
        
        -clusters (default 3)     -Number of clusters to generate
        -vectors (default 1000)   -Number of vectors to generate
        -dim (default 100)        -Number of significant columns to generate

        -charts (default pdf)        -Generated chart format (save, show, none, all, png, pdf)
        -output (default all)        -Output 'all' or 'minimal' files (generator)
        -param  (default 'vectors')  -Parameter to add to csv output; can be any other parameter
    ____________________________________
    
    **Noise Options**
        -noise (default 0%) (0-1)      -Amount of noise to add to final output
        -featnoise (default 0%) (0-1)   -Percentage of uncorrelated features to generate
        -vectnoise (default 0%) (0-1)  -Percentage of uncorrelated vectors to generate
    ___________________________________

    **Generation Distribution Options**
        -dist (default gauss)    -Distribution to generate points on
            -gauss or normal        -Generate points on gaussian distribution
            -uniform or uni         -Generate points uniformly
            -binomial or binom      -Generate points using a binomial distribution
            -exponential or exp     -Generate points using an exponential distribution
    ____________________________________
   
    **CENTROID OPTIONS**
        -corg (default random)     -Organization of clusters to be generated (pairs, triplets, etc.)
                                       -random, bi, tri, quad, all
        -cdist (default .4)        -Target distance of cluster centroid orgs
        -csigma (default .1)       -Deviation of a cluster
        -ccounts (default random)  -Cluster counts to partition total vectors into
                                       -random, equal, (TODO)separated
    ____________________________________
    
    **Test Sequence Multithreading**
        -multithread (default false)    -Run multithreaded test sequences (python limits 1 sequence per core)
        -threads (default 2)            -Max number of threads to spawn
    ____________________________________

    **Output Randomization Options**
        -rshuf (default true)  (true, false) -Randomize the vectors (Rows)
        -cshuf (default random) (separated, intermixed, random)
                                    -Determine how to shuffle the columns; separated keeps significant
                                        columns stacked on low indexed features and dummy columns on 
                                        high indexed features; intermixed disperses evenly; random
                                        performs a shuffle on the columns
        -noise (default 0%) (0-1)      -Amount of noise to add to final output
        -featnoise (default 0%) (0-1)   -Percentage of uncorrelated features to generate
        -vectnoise (default 0%) (0-1)  -Percentage of uncorrelated vectors to generate
    ____________________________________    
    
    **Cluster Evolution Options** (IN PROGRESS)
        -evolve (default false) (true, false) -Turn on cluster evolution
        -evint (default 250) -interval to change clusters on
        -evtype (default random) -evolution type (random, *shift - *NOT IMPLEMENTED
    ____________________________________
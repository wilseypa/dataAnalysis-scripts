library(streamMOA)
library(TDA)

dataStream <- DSD_ReadCSV(file = "testData.csv", k = 14, class = 35, header = TRUE)

denStream <- DSC_DenStream(epsilon = 0.25, mu = 1, beta = 0.2, lambda = 0.01, initPoints = 100, offline = 2, processingSpeed = 1, recluster = TRUE)

epoch <- 500
pos <- 1

while ( dim( get_points(dataStream, n = 1, outofpoints = "ignore") )[1] != 0 ) {
  reset_stream( dataStream, pos )
  update( denStream, dataStream, epoch )
  pos <- pos + epoch
  reset_stream( stream, pos - epoch )
  points <- get_points( dataStream, n = epoch )
  
  reset_stream( stream, pos - epoch )
  clusterLabels <- get_assignment( denStream, points, type = "macro" )
  points$clusterLabels <- clusterLabels
}
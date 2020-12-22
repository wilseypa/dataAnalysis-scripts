library(streamMOA)
library(TDA)
library(mclust)

dataStream <- DSD_ReadCSV(file = "testData.csv", k = 19, class = 35, header = TRUE)
dataStreamWithLabels <- DSD_ReadCSV(file = "testData.csv", k = 19, header = TRUE)

denStream <- DSC_DenStream(epsilon = 0.25, mu = 1, beta = 0.2, lambda = 0.01, initPoints = 200, offline = 20, processingSpeed = 1, recluster = TRUE)

epoch <- 500
pos <- 1
t <- 0

eps <- 5
maxDimension <- 1

while ( dim( get_points(dataStream, n = 1, outofpoints = "ignore") )[1] != 0 ) {
  t <- t + 1
  reset_stream( dataStream, pos )
  update( denStream, dataStream, epoch )
  pos <- pos + epoch
  reset_stream( dataStream, pos - epoch )
  points <- get_points( dataStream, n = epoch )
  
  clusterLabels <- get_assignment( denStream, points, type = "macro" )
  points$clusterLabels <- clusterLabels
  
  # For evaluation of clustering.
  pointsWithLabels <- get_points( dataStreamWithLabels, n = epoch )
  groundTruth <- pointsWithLabels$type
  ari <- adjustedRandIndex(clusterLabels, groundTruth)
  print(paste(t, ":", ari))
  
  uniqueClusters <- unique(clusterLabels)
  
  pdf(file = paste0("output/time", t), width = 11, height = 8.50)
  for (clust in uniqueClusters) {
    # clustName <- paste("cluster", clust, sep = "")
    # assign(clustName, points[points$clusterLabels == clust, ])
    cluster <- points[points$clusterLabels == clust, ]
    cluster$clusterLabels <- NULL
    Diag <- ripsDiag(X = cluster, maxDimension, eps, library = "GUDHI", printProgress = FALSE)
    par(col.lab = "white")
    plot(Diag[["diagram"]], barcode = TRUE)
    par(col.lab = "black")
    title(main = paste("Barcodes: Cluster", clust), xlab = expression(epsilon))
    legend("right", inset = 0.08, legend = c(expression(H[0]), expression(H[1])), col = c("black", "red"), lty = 1, lwd = 1.5, cex = 0.9, box.lty = 0)
  }
  dev.off()
}
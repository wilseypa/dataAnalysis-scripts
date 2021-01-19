library(streamMOA)
library(TDA)
library(ggplot2)

stream <- DSD_ReadCSV(file = "subsetKDDtinyWindow.csv", header = TRUE)

reset_stream(stream)
ct <- DSC_ClusTree(horizon = 11, maxHeight = 10, lambda = NULL, k = NULL)

maxDimension <- 1
eps <- 4

wasserp2d11 <- numeric(100)
wasserp2d12 <- numeric(100)
streamProgress <- integer(100)

# pdf(file = "~/Desktop/Plots.pdf", width = 11, height = 8.50)

for (i in 1:101) {
  update(ct, stream, 10)
  centers <- data.matrix(na.omit(get_centers(ct, type = "micro")))
  print(paste("Number of microcluster centers:", nrow(centers)))
  currDiag <- ripsDiag(X = centers, maxDimension, eps, library = "GUDHI",
                       printProgress = FALSE)
  if (i == 1) {
    refDiag <- currDiag
  }
  
  if (i > 1) {
    distance1 <- wasserstein(prevDiag[["diagram"]], currDiag[["diagram"]],
                             p = 2, dimension = 0)
    distance2 <- wasserstein(refDiag[["diagram"]], currDiag[["diagram"]],
                             p = 2, dimension = 0)
    wasserp2d11[i-1] <- distance1
    wasserp2d12[i-1] <- distance2
    
    streamProgress[i-1] <- i*10
  }
  prevDiag <- currDiag
}


# dev.off()
close_stream(stream)


dfp2d11 <- data.frame(
  stream = streamProgress,
  distance = wasserp2d11
)

dfp2d12 <- data.frame(
  stream = streamProgress,
  distance = wasserp2d12
)


plot1 <- ggplot(dfp2d11, aes(x = stream, y = distance)) +
  geom_line(color = 'darkorchid4') +
  scale_x_continuous(breaks = scales::pretty_breaks(n = 8)) +
  # scale_x_continuous(breaks = scales::pretty_breaks(n = 21)) +
  labs(x = "Progress of Stream", y = "1-dimensional 2nd Wasserstein Distance",
       title = "Wasserstein Distances between Pairs of Consecutive Persistence Diagrams")

print(plot1)


plot2 <- ggplot(dfp2d12, aes(x = stream, y = distance)) +
  geom_line(color = 'coral4') +
  scale_x_continuous(breaks = scales::pretty_breaks(n = 8)) +
  # scale_x_continuous(breaks = scales::pretty_breaks(n = 21)) +
  labs(x = "Progress of Stream", y = "0-dimensional 2nd Wasserstein Distance",
       title = "Wasserstein Distances between Persistence Diagrams of Reference Normal Connection and Subsequent Connections")

print(plot2)
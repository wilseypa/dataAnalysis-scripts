library(streamMOA)
library(TDA)
library(ggplot2)

stream <- DSD_ReadCSV(file = "newShuffledStream.csv", header = TRUE)

reset_stream(stream)
ct <- DSC_ClusTree(horizon = 450, maxHeight = 10, lambda = NULL, k = NULL)

maxDimension <- 1
eps <- 0.15

wasserp2d11 <- numeric(9)
wasserp2d12 <- numeric(9)
streamProgress <- integer(9)

# pdf(file = "~/Desktop/Plots.pdf", width = 11, height = 8.50)

for (i in 1:9) {
  update(ct, stream, 1000)
  centers <- data.matrix(na.omit(get_centers(ct, type = "micro")))
  currDiag <- ripsDiag(X = centers, maxDimension, eps, library = "GUDHI",
                       printProgress = FALSE)
  if (i == 1) {
    refDiag <- currDiag
  }
  
  if (i > 1) {
    distance1 <- bottleneck(prevDiag[["diagram"]], currDiag[["diagram"]],
                            dimension = 1)
    distance2 <- bottleneck(refDiag[["diagram"]], currDiag[["diagram"]],
                            dimension = 1)
    wasserp2d11[i-1] <- distance1
    wasserp2d12[i-1] <- distance2
    
    streamProgress[i-1] <- i*1000
  }
  prevDiag <- currDiag
}

update(ct, stream, 350)
centers <- data.matrix(na.omit(get_centers(ct, type = "micro")))

currDiag <- ripsDiag(X = centers, maxDimension, eps, library = "GUDHI",
                     printProgress = FALSE)

distance1 <- bottleneck(prevDiag[["diagram"]], currDiag[["diagram"]],
                        dimension = 1)
distance2 <- bottleneck(refDiag[["diagram"]], currDiag[["diagram"]],
                        dimension = 1)

wasserp2d11[i] <- distance1
wasserp2d12[i] <- distance2

streamProgress[i] <- i*1000 + 350

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
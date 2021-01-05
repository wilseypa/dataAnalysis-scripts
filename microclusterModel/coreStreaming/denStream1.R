library(streamMOA)
library(TDA)

stream <- DSD_ReadCSV(file = "/home/anindya/Data/UC/Research/TDA/DataSets/streaming/ViralEvolution/stream2/newShuffledStream.csv", header = TRUE)
data <- read.csv("/home/anindya/Data/UC/Research/TDA/DataSets/streaming/ViralEvolution/stream2/newShuffledStream.csv", header = TRUE)
data <- data.matrix(data)

reset_stream(stream)
denStream <- DSC_DenStream(epsilon = 0.03, mu = 5, beta = 0.2, lambda = 0.2, initPoints = 500, processingSpeed = 1, recluster = FALSE)

for (i in 1:9) {
  update(denStream, stream, 1000)
  centers <- data.matrix(na.omit(get_centers(denStream, type = "micro")))
  print(nrow(centers))
  
  plot(data[((i-1)*1000 + 1):(i*1000),], col = "goldenrod1")
  points(centers, col = "blue")
}

update(denStream, stream, 350)
centers <- data.matrix(na.omit(get_centers(denStream, type = "micro")))
print(nrow(centers))
plot(centers, col = "blue")


close_stream(stream)
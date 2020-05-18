library(streamMOA)
library(TDA)

stream <- DSD_ReadCSV(file = "/home/anindya/Data/UC/Research/TDA/DataSets/streaming/ViralEvolution/stream2/totalStream.csv", header = TRUE)
data <- read.csv("/home/anindya/Data/UC/Research/TDA/DataSets/streaming/ViralEvolution/stream2/totalStream.csv", header = TRUE)
data <- data.matrix(data)

reset_stream(stream)
streamKm <- DSC_StreamKM(sizeCoreset = 9350, numClusters = 200, length = 9350)

for (i in 1:9) {
  update(streamKm, stream, 1000)
  centers <- data.matrix(na.omit(get_centers(streamKm, type = "macro")))
  print(nrow(centers))
  
  plot(data[((i-1)*1000 + 1):(i*1000),], col = "goldenrod1")
  points(centers, col = "blue")
}

update(streamKm, stream, 350)
centers <- data.matrix(na.omit(get_centers(streamKm, type = "macro")))
print(nrow(centers))
plot(centers, col = "blue", xlim = c(-0.1, 0.1), ylim = c(-0.12, 0.07))


close_stream(stream)
library(streamMOA)
library(TDA)

stream <- DSD_ReadCSV(file = "/home/anindya/Data/UC/Research/TDA/DataSets/streaming/ViralEvolution/stream2/totalStream.csv", header = TRUE)
data <- read.csv("/home/anindya/Data/UC/Research/TDA/DataSets/streaming/ViralEvolution/stream2/totalStream.csv", header = TRUE)
data <- data.matrix(data)

reset_stream(stream)
bico <- DSC_BICO_MOA(Cluster = 200, Dimensions = 45)

for (i in 1:9) {
  update(bico, stream, 1000)
  centers <- data.matrix(na.omit(get_centers(bico, type = "micro")))
  print(nrow(centers))
  
  plot(data[((i-1)*1000 + 1):(i*1000),], col = "goldenrod1")
  points(centers, col = "blue")
}

update(bico, stream, 350)
centers <- data.matrix(na.omit(get_centers(bico, type = "micro")))
print(nrow(centers))
plot(centers, col = "blue", xlim = c(-0.1, 0.1), ylim = c(-0.12, 0.07))


close_stream(stream)
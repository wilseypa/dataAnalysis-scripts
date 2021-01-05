library(streamMOA)
library(TDA)

stream <- DSD_ReadCSV(file = "/home/anindya/Data/UC/Research/TDA/DataSets/streaming/ViralEvolution/stream2/newShuffledStream.csv", header = TRUE)
data <- read.csv("/home/anindya/Data/UC/Research/TDA/DataSets/streaming/ViralEvolution/stream2/newShuffledStream.csv", header = TRUE)
data <- data.matrix(data)

reset_stream(stream)
ct <- DSC_ClusTree(horizon = 450, maxHeight = 10, lambda = NULL, k = NULL)

maxDimension <- 1
eps <- 0.17

layout(matrix(c(1,2,2,3,4,4), nrow = 2, ncol = 3, byrow = TRUE))

for (i in 1:9) {
  update(ct, stream, 1000)
  centers <- data.matrix(na.omit(get_centers(ct, type = "micro")))
  print(nrow(centers))
  
  plot(data[((i-1)*1000 + 1):(i*1000),], col = "azure3", xlim = c(-0.1, 0.1), ylim = c(-0.12, 0.1), pch = 16)
  points(centers, col = "coral", pch = 3)
  title(main = paste("Stream:", ((i-1)*1000 + 1), "-", i*1000))
  legend("topleft", inset = 0.01, legend = c("Data points", "Microcluster centers"), col = c("azure3", "coral"), pch = c(16,3), box.lty = 0)
  
  Diag <- ripsDiag(X = centers, maxDimension, eps, library = "GUDHI", printProgress = FALSE)
  
  par(col.lab = "white")
  plot(Diag[["diagram"]], barcode = TRUE)
  par(col.lab = "black")
  title(main = paste("Barcodes at", i*1000, "Points"), xlab = expression(epsilon))
  legend("bottomright", inset = 0.08, legend = c(expression(H[0]), expression(H[1])), col = c("black", "red"), lty = 1, lwd = 1.5, cex = 0.9, box.lty = 0)
}

update(ct, stream, 350)
centers <- data.matrix(na.omit(get_centers(ct, type = "micro")))
print(nrow(centers))

plot(data[9001:9350,], col = "azure3", xlim = c(-0.1, 0.1), ylim = c(-0.12, 0.1), pch = 16)
points(centers, col = "coral", pch = 3)
title(main = paste("Stream:", 9001, "-", 9350))
legend("topleft", inset = 0.01, legend = c("Data points", "Microcluster centers"), col = c("azure3", "coral"), pch = c(16,3), box.lty = 0)

Diag <- ripsDiag(X = centers, maxDimension, eps, library = "GUDHI", printProgress = FALSE)

par(col.lab = "white")
plot(Diag[["diagram"]], barcode = TRUE)
par(col.lab = "black")
title(main = "Barcodes at 9350 Points", xlab = expression(epsilon))
legend("bottomright", inset = 0.08, legend = c(expression(H[0]), expression(H[1])), col = c("black", "red"), lty = 1, lwd = 1.5, cex = 0.9, box.lty = 0)

close_stream(stream)
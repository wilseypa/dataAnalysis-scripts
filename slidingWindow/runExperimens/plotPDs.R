library(TDA)

maxDimension <- 1
eps <- 0.15

offlineInterval <- 600
fileNums <- c(0:9)

pdf(file = "~/Desktop/Plots.pdf", width =  8.50, height = 11)
par(mfrow = c(3, 2), mai=c(0.6, 0.56, 0.25, 0.15))

for (num in fileNums) {
  swVals <- read.csv(
    file = paste0("outputHIV/SlidingWindow_", num, "_output.csv"),
    header = FALSE
  )
  
  swVals[,ncol(swVals)] <- NULL
  Diag <- ripsDiag(X = swVals, maxDimension, eps, library = "GUDHI",
                   printProgress = FALSE)
  
  par(col.lab = "white")
  plot(Diag[["diagram"]], band = 0.01, colorBand = "palegoldenrod",
       panel.first = grid(NULL, NULL, lty = 1, col = "lightgray"))
  par(col.lab = "black")
  
  title(main = paste("Persistence Diagram at", (num+1)*offlineInterval, "Points"),
        xlab = expression(epsilon[birth]), ylab = expression(epsilon[death]),
        cex.lab = 1.4, cex.main = 1.2)
  legend("bottomright", inset = 0.08,
         legend = c(expression(H[0]), expression(H[1])),
         col = c("black", "red"), lty = 0, lwd = 1.5, pch = c(16, 2),
         cex = 1.1, bty = "n")
}



swVals <- read.csv(file = "outputHIV/SlidingWindow_10_output.csv", header = FALSE)

swVals[,ncol(swVals)] <- NULL
Diag <- ripsDiag(X = swVals, maxDimension, eps, library = "GUDHI",
                 printProgress = FALSE)

par(col.lab = "white")
plot(Diag[["diagram"]], band = 0.01, colorBand = "palegoldenrod",
     panel.first = grid(NULL, NULL, lty = 1, col = "lightgray"))
par(col.lab = "black")

title(main = "Persistence Diagram at 6122 Points",
      xlab = expression(epsilon[birth]), ylab = expression(epsilon[death]),
      cex.lab = 1.4, cex.main = 1.2)
legend("bottomright", inset = 0.08,
       legend = c(expression(H[0]), expression(H[1])),
       col = c("black", "red"), lty = 0, lwd = 1.5, pch = c(16, 2),
       cex = 1.1, bty = "n")

dev.off()
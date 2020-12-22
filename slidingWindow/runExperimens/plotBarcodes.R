library(TDA)

maxDimension <- 1
eps <- 4
offlineInterval <- 10

normalFileNums <- c(18, 31, 48, 58, 78, 98)

pdf(file = "~/Desktop/Plots.pdf", width =  8.50, height = 11)
par(mfrow = c(3, 2), mai=c(0.6, 0.1, 0.25, 0.1))

for (num in normalFileNums) {
  swVals <- read.csv(
    file = paste0("outputKDD/SlidingWindow_", num, "_output.csv"), header = FALSE
  )
  
  swVals[,ncol(swVals)] <- NULL
  Diag <- ripsDiag(X = swVals, maxDimension, eps, library = "GUDHI", printProgress = FALSE)
  
  par(col.lab = "white")
  plot(Diag[["diagram"]], barcode = TRUE)
  par(col.lab = "black")
  title(main = paste("Normal Traffic: Barcodes at", (num+1)*offlineInterval, "Points"),
        xlab = expression(epsilon))
  legend("topright", inset = 0.08, legend = c(expression(H[0]), expression(H[1])),
         col = c("black", "red"), lty = 1, lwd = 1.5, cex = 0.9, box.lty = 0)
}

attackFileNums <- c(20, 21, 34, 50, 61, 80)
attackNames <- c('guess_passwd', 'guess_passwd', 'buffer_overflow', 'imap',
                 'rootkit', 'warezmaster')
i <- 1
for (num in attackFileNums) {
  swVals <- read.csv(
    file = paste0("outputKDD/SlidingWindow_", num, "_output.csv"), header = FALSE
  )
  
  swVals[,ncol(swVals)] <- NULL
  Diag <- ripsDiag(X = swVals, maxDimension, eps, library = "GUDHI", printProgress = FALSE)
  
  par(col.lab = "white")
  plot(Diag[["diagram"]], barcode = TRUE)
  par(col.lab = "black")
  title(main = paste(attackNames[i], "Attack: Barcodes at", (num+1)*offlineInterval, "Points"),
        xlab = expression(epsilon))
  legend("topright", inset = 0.08, legend = c(expression(H[0]), expression(H[1])),
         col = c("black", "red"), lty = 1, lwd = 1.5, cex = 0.9, box.lty = 0)
  i <- i + 1
}

dev.off()
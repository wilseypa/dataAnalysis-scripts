require(clValid)
require(mclust)
require(fpc)

args <- commandArgs(TRUE)
srcFile <- args[1]
csvDir <- args[2]
outputFile <- args[3]
outputFile2 <- args[4]

data <- read.csv(srcFile, header = FALSE)
gt <- data[,ncol(data)]
data.features <- data
data.features[, ncol(data.features)] <- NULL
d <- dist(data.features, method = "euclidean")

funcPurity <- function(clusterLabels, groundTruthLabels) {
  sum(apply(table(groundTruthLabels, clusterLabels), 2, max)) / length(clusterLabels)
}

n <- 6

ari <- vector()
purity <- vector()
silWidth <- vector()
wcsse <- vector()
runtimes <- vector()
memory <- vector()

files <- list.files(path = csvDir, pattern = "*.csv", full.names = TRUE)
lapply(files, function(i) {
  f <- read.csv(i, header = FALSE)
  if (ncol(f) == n) {
    for (j in 1:n) {
      ari[j] <- adjustedRandIndex(f[,j], gt)
      purity[j] <- funcPurity(f[,j], gt)
      
       if (length(unique(f[,j])) != 1) {
         sil <- silhouette(f[,j], d)
         silWidth[j] <- summary(sil)$si.summary['Mean']
         validations <- cluster.stats(d, f[,j])
         wcsse[j] <- validations$within.cluster.ss
     }
       else {
         sink(file = "Message.txt")
         print(paste0(i, "Config detected only one cluster at run ", j), quote = FALSE)
         sink()
       }
   }

    ari_mean <- mean(ari)
    purity_mean <- mean(purity)
    ari_sd <- sd(ari)
    purity_sd <- sd(purity)
     silWidth_mean <- mean(silWidth)
     silWidth_sd <- sd(silWidth)
     wcsse_mean <- mean(wcsse)
     wcsse_sd <- sd(wcsse)
    row1 <- paste0(i, ",", ari[1], ",", ari[2], ",", ari[3], ",", ari[4], ",", ari[5], ",", ari[6], "," ,ari_mean, ",", ari_sd, ",", ari_sd/ari_mean, ",",
                   purity[1],",",purity[2],",",purity[3],",",purity[4],",",purity[5],",",purity[6],",",purity_mean, ",", purity_sd ,",", purity_sd/purity_mean, ",",
				   silWidth[1], ",", silWidth[2], ",", silWidth[3], ",", silWidth[4], ",", silWidth[5], ",", silWidth[6],  "," , silWidth_mean , ",", silWidth_sd/silWidth_mean, ",",
				   silWidth_sd, "," , wcsse[1], ",", wcsse[2], ",", wcsse[3], ",", wcsse[4], ",", wcsse[5], ",", wcsse[6], "," ,wcsse_mean, ",", wcsse_sd, "," , wcsse_sd/wcsse_mean
				   )
    write.table(row1, file = outputFile, append = TRUE, quote = FALSE, sep = ",",
                row.names = FALSE, col.names = FALSE)
  }
  if (ncol(f) == 18) {
    for (k in 1:n) {
      runtimes[k] <- f[1, 3*k-2]
      memory[k] <- f[1, 3*k-1]
    }
    runtimes_mean <- mean(runtimes)
    sd_run <- sd(runtimes)
    memory_mean <- mean(memory)
    sd_mem <- sd(memory)
    row2 <- paste0(i, ",",runtimes[1],",",runtimes[2],",",runtimes[3],",",runtimes[4],",",runtimes[5],",",runtimes[6],",", runtimes_mean,",",
                   sd_run,",",memory[1],",",memory[2],",",memory[3],",",memory[4],",",memory[5],",",memory[6],",",memory_mean, ",",sd_mem)
    write.table(row2, file = outputFile2, append = TRUE, quote = FALSE, sep = ",",
                row.names = FALSE, col.names = FALSE)
  }
})

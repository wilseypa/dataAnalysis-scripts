library(TDA)
library(ggplot2)

refOutput1 <- read.csv("outputKDD/FastPersistence_bettis_output_98.csv",
                      header = FALSE)  # ipsweep
refOutput1 <- data.matrix(refOutput1)


refOutput2 <- read.csv("outputKDD/FastPersistence_bettis_output_113.csv",
                       header = FALSE)  # satan
refOutput2 <- data.matrix(refOutput2)

numDist <- 129

wasserp2d01 <- numeric(numDist)
wasserp2d02 <- numeric(numDist)
streamProgress <- integer(numDist)

offlineInterval <- 200

for (i in 0:(numDist-1)) {
  curOutput <- read.csv(
    file = paste0("outputKDD/FastPersistence_bettis_output_", i, ".csv"), header = FALSE
  )
  curOutput <- data.matrix(curOutput)
  
  distance1 <- wasserstein(refOutput1, curOutput, p = 2, dimension = 0)
  distance2 <- wasserstein(refOutput2, curOutput, p = 2, dimension = 0)
  
  wasserp2d01[i] <- distance1
  wasserp2d02[i] <- distance2
  
  streamProgress[i] <- (i+1)*offlineInterval
}


dfp2d01 <- data.frame(
  stream = streamProgress,
  distance = wasserp2d01
)


dfp2d02 <- data.frame(
  stream = streamProgress,
  distance = wasserp2d02
)

plot1 <- ggplot(dfp2d01, aes(x = stream, y = distance)) +
  geom_line(color = 'darkorchid4') +
  scale_x_continuous(breaks = scales::pretty_breaks(n = 13)) +
  # scale_x_continuous(breaks = scales::pretty_breaks(n = 21)) +
  labs(x = "Progress of Stream", y = "0-dimensional 2nd Wasserstein Distance",
       title = "Wasserstein Distances between Persistence Diagrams of Reference ipsweep Attack and Other Traffics")

print(plot1)

plot2 <- ggplot(dfp2d02, aes(x = stream, y = distance)) +
  geom_line(color = 'coral4') +
  scale_x_continuous(breaks = scales::pretty_breaks(n = 13)) +
  # scale_x_continuous(breaks = scales::pretty_breaks(n = 21)) +
  labs(x = "Progress of Stream", y = "0-dimensional 2nd Wasserstein Distance",
       title = "Wasserstein Distances between Persistence Diagrams of Reference satan Attack and Other Traffics")

print(plot2)
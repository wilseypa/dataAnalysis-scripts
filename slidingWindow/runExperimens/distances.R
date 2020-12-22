library(TDA)
library(ggplot2)
# require(gridExtra)

prevOutput <- read.csv("outputKDD/FastPersistence_bettis_output_0.csv", header = FALSE)
prevOutput <- data.matrix(prevOutput)

refOutput <- prevOutput

# refOutput <- read.csv("outputKDD/FastPersistence_bettis_output_15.csv", header = FALSE)  # Smurf
# refOutput <- data.matrix(refOutput)

numDist <- 128
# numDist <- 100
# numDist <- 1566

wasserp2d01 <- numeric(numDist)
wasserp2d02 <- numeric(numDist)
streamProgress <- integer(numDist)

offlineInterval <- 200
# offlineInterval <- 10

for (i in 1:numDist) {
  curOutput <- read.csv(
    file = paste0("outputNSL/FastPersistence_bettis_output_", i, ".csv"), header = FALSE
    )
  curOutput <- data.matrix(curOutput)
  
  distance1 <- wasserstein(prevOutput, curOutput, p = 2, dimension = 0)
  distance2 <- wasserstein(refOutput, curOutput, p = 2, dimension = 0)
  
  wasserp2d01[i] <- distance1
  wasserp2d02[i] <- distance2
  
  prevOutput <- curOutput
  
  streamProgress[i] <- (i+1)*offlineInterval
}

# plot(wasserp2d0, type = "l")
# plot(wasserp2d01, type = "l")

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
       title = "Wasserstein Distances between Pairs of Consecutive Persistence Diagrams")

print(plot1)

plot2 <- ggplot(dfp2d02, aes(x = stream, y = distance)) +
  geom_line(color = 'coral4') +
  scale_x_continuous(breaks = scales::pretty_breaks(n = 13)) +
  # scale_x_continuous(breaks = scales::pretty_breaks(n = 21)) +
  labs(x = "Progress of Stream", y = "0-dimensional 2nd Wasserstein Distance",
       title = "Wasserstein Distances between Persistence Diagrams of Reference smurf Attack and Other Traffics")

print(plot2)
# grid.arrange(plot1, plot2, ncol = 1, nrow = 2)
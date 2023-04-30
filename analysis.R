library(tidyverse)
library(extrafont) # font embedding
library(gridExtra)
rm(list=ls())
setwd("~/csboy/ditransitive/")

library(rwebppl)

wppl_files <- list("NoCostNoPrior",
                   "CostNoPrior",
                   "NoCostPrior",
                   "CostPrior")
data <- list()

priors_likely <- read.csv("priors/priors_likely.csv", sep = '\t')
priors_unlikely <- read.csv("priors/priors_unlikely.csv", sep = '\t')

for (file in wppl_files) {
  # read data:
  temp <- webppl(program_file = paste0("models/", file, ".wppl"),
                      data = df)
  if (!grepl("NoPrior", file)) {
    for (i in 1:nrow(temp)) {
      # load in and multiply by priors:
      temp[i, 2] <- temp[i, 2] * priors_likely[i, 2]
    }
    # normalize
    temp$prob <- scale(temp$prob, center = FALSE, scale = sum(temp$prob))
  }
  data[[file]] <- temp
}

plot_list <- list()
for (name in names(data)) {
  p <- ggplot(data[[name]],
              aes(x = support,
                  y = prob,
                  fill = support)) +
    geom_bar(stat = "identity") +
    ggtitle(name) +
    labs(x = "", y = "Probability") +
    theme(legend.position = "none")
  plot_list[[length(plot_list) + 1]] <- p
}

# Combine all ggplot objects into a single plot using grid.arrange()
g <- arrangeGrob(grobs = plot_list)

ggsave("plots/probabilities_likely.pdf", g, width=6, height=6, units = "in", dpi = 300)
library(tidyverse)
library(extrafont) # font embedding
library(gridExtra)
library(viridis)
rm(list=ls())
setwd("~/csboy/ditransitive/")

library(rwebppl)

dfs <- list()
informativities = c('low', 'med', 'high')
priors <- c(0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75)
costs <- c(0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75)
for (i in informativities) {
  idf <- data.frame(double(), double(), double(), double())
  names(idf) <- c('prior', 'cost', 'informativity', 'prob')
  for (p in priors) {
    for (cost in costs) {
      settings <- data.frame(recipientprior = p, recipientcost = cost, informativity = i)
      output <- c(webppl(program_file = 'models/model.js', data = settings, data_var = "dataFromR"))
      idf[nrow(idf) + 1,] <- c(p, cost, i, data.frame(prob = output)[1, 'prob'])
    }
  }
  dfs[[i]] <- idf
}

combined_df <- do.call(rbind, dfs)
combined_df$prior <- as.numeric(combined_df$prior)
combined_df$cost <- as.numeric(combined_df$cost)
combined_df$prob <- as.numeric(combined_df$prob)
combined_df$informativity <- factor(combined_df$informativity)

ggplot(combined_df, aes(x = prior, y = cost, fill = prob)) +
  geom_tile() +
  scale_fill_viridis() +
  labs(x = "prior probability of recipient", y = "cost of recipient", fill = "probability") +
  facet_wrap(~factor(informativity, levels=c('low', 'med', 'high')))

ggplot(combined_df, aes(x = cost, y = prob)) +
  geom_bar(stat = 'identity') +
  ylim(0, 1) +
  facet_wrap(~factor(informativity, levels=c('low', 'med', 'high')))

ggplot(combined_df, aes(x = cost, y = prob)) +
  geom_bar(stat = 'identity') +
  ylim(0, 1) +
  facet_wrap(~factor(informativity, levels=c('low', 'med', 'high')))

for (df in dfs) {
  combined_df <- bind_rows(combined_df, df, .id = "source")
}

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
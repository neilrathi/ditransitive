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
  geom_ti() +
  scale_fill_viridis() +
  labs(x = "prior probability of recipient", y = "cost of recipient", fill = "probability") +
  facet_wrap(~factor(informativity, levels=c('low', 'med', 'high')))

ggplot(combined_df, aes(x = prior, y = prob)) +
  geom_bar(stat = 'identity') +
  facet_wrap(~factor(informativity, levels=c('low', 'med', 'high')))

for (df in dfs) {
  combined_df <- bind_rows(combined_df, df, .id = "source")
}

ggsave("plots/probabilities_likely.pdf", g, width=6, height=6, units = "in", dpi = 300)
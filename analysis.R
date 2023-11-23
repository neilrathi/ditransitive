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


dfs <- list()
informativities = c('low', 'high')
for (i in informativities) {
  idf <- data.frame(double(), double(), double())
  names(idf) <- c('informativity', 'prob', 'tr')
  settings <- data.frame(informativity = i)
  output <- c(webppl(program_file = 'models/simple_model.js', data = settings, data_var = "dataFromR"))
  idf[nrow(idf) + 1,] <- c(i, data.frame(prob = output)[1, 'prob'], 'recipient')
  idf[nrow(idf) + 1,] <- c(i, data.frame(prob = output)[2, 'prob'], 'theme')
  dfs[[i]] <- idf
}

combined_df <- do.call(rbind, dfs)
combined_df$prob <- as.numeric(combined_df$prob)
combined_df$informativity <- factor(combined_df$informativity)

small_df <- data.frame(informativity = c("control", "control"), prob = c(0.5, 0.5), tr = c("recipient", "theme"))
total_df <- rbind(combined_df, small_df)

ggplot(total_df, aes(x = tr, y = prob, fill = tr)) +
  geom_bar(stat = 'identity') +
  ylab('Production Probability') +
  xlab('Constituent') +
  theme(legend.position="bottom",
        axis.text.x = element_blank(),
        axis.title.x = element_blank(),
        axis.ticks.x=element_blank(),
        legend.title = element_blank()) +
  facet_wrap(~factor(informativity, levels=c('control', 'low', 'med', 'high'))) +
  scale_y_continuous(breaks = seq(0, 1, .1), limits = c(0, 1)) +
  geom_hline(yintercept = 0, linewidth = .3)

for (df in dfs) {
  combined_df <- bind_rows(combined_df, df, .id = "source")
}

ggsave("plots/informativity.png", width=6, height=4, units = "in", dpi = 300)

rm(list=ls())
setwd("~/csboy/ditransitive/analysis")

library(tidyverse)
library(extrafont) # font embedding

library(lme4)
library(boot)
library(ggthemes)

### IMPORT DATAFRAME ###
df <- read.csv('complete_clean.csv', sep = '\t')
df$item <- paste(df$agent, df$verb, df$theme, df$recipient)

### COMPUTE MIXED EFFECTS LOGISTIC REGRESSION ###
model <- glmer(factor(order) ~ informativity +
                 (1 + informativity || gameID) +
                 (1 + informativity || item),
               data = df,
               family = "binomial")

### PLOTS + BOOTSTRAP STATISTICS ###
df %>%
  count(order)

# get actual proportions
by_verb_actual <- df %>%
  group_by(verb) %>%
  summarize(
    PO_actual = sum(order == "PO") / n(),
    DO_actual = sum(order == "DO") / n()
  )

by_informativity_actual <- df %>%
  group_by(informativity) %>%
  summarize(
    PO_actual = sum(order == "PO") / n(),
    DO_actual = sum(order == "DO") / n()
  )

# bootstrap 95% CI by condition
prop <- function(data, indices) {
  dt <- data[indices, ]
  prop_PO <- sum(dt$order == "PO") / nrow(dt)
  prop_DO <- sum(dt$order == "DO") / nrow(dt)
  c(prop_PO,
    prop_DO)
}

set.seed(12345)

by_verb_ci <- df %>% 
  group_by(verb) %>% 
  do({
    boot_verb <- boot(data = .,
                      statistic = prop,
                      R = 1000)
    
    ci_PO <- boot.ci(boot_verb, type = "perc", index = 1)
    ci_DO <- boot.ci(boot_verb, type = "perc", index = 2)
    
    data.frame(verb = unique(.$verb),
               PO_lower = ci_PO$perc[4],
               PO_upper = ci_PO$perc[5],
               DO_lower = ci_DO$perc[4],
               DO_upper = ci_DO$perc[5])
  })

by_informativity_ci <- df %>% 
  group_by(informativity) %>% 
  do({
    boot_verb <- boot(data = .,
                      statistic = prop,
                      R = 1000)
    
    ci_PO <- boot.ci(boot_verb, type = "perc", index = 1)
    ci_DO <- boot.ci(boot_verb, type = "perc", index = 2)
    
    data.frame(informativity = unique(.$informativity),
               PO_lower = ci_PO$perc[4],
               PO_upper = ci_PO$perc[5],
               DO_lower = ci_DO$perc[4],
               DO_upper = ci_DO$perc[5])
  })


by_verb <- left_join(by_verb_actual, by_verb_ci, by = "verb")
by_informativity <- left_join(by_informativity_actual, by_informativity_ci, by = "informativity")


# long versions of each df for plotting
long_by_verb <- by_verb %>%
  gather(key = "measure", value = "value", PO_actual:DO_upper) %>%
  separate(measure, into = c("order", "measure"), sep = "_") %>%
  spread(key = "measure", value = "value")

long_by_informativity <- by_informativity %>%
  gather(key = "measure", value = "value", PO_actual:DO_upper) %>%
  separate(measure, into = c("order", "measure"), sep = "_") %>%
  spread(key = "measure", value = "value")

ggplot(long_by_verb, aes(x = order, fill = order, y = actual, ymin = lower, ymax = upper)) +
  geom_col() +
  scale_fill_manual("legend", values = c("#d78691",  "#72b072")) +
  geom_errorbar(width = 0.2) +
  facet_wrap(~ verb) +
  labs(x = "order", y = "prop") +
  theme_bw()

ggplot(long_by_informativity, aes(x = order, fill = order, y = actual, ymin = lower, ymax = upper)) +
  geom_col() +
  scale_fill_manual("legend", values = c("#d78691",  "#72b072")) +
  geom_errorbar(width = 0.2) +
  facet_wrap(~ informativity) +
  labs(x = "order", y = "prop") +
  theme_bw()
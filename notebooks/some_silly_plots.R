library(tidyverse)
library(ggplot2)

song_data <- read.csv("data\\playlist_song_list_recommender_ids.tsv", sep = "\t")

song_data %>%
  ggplot(aes(x = year)) + 
  geom_histogram()
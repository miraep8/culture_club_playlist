library(tidyverse)
library(ggplot2)
library(phyloseq)
library(microViz)

song_data <- read.csv("data\\playlist_song_list_recommender_ids.tsv", sep = "\t") %>%
  mutate(recommender_factor = as.factor(recommender_id))

song_data %>%
  ggplot(aes(x = year, fill = recommender_factor)) +
  geom_histogram() + 
  theme_classic() + 
  labs(
    x = "Year Song was Released",
    y = "Number of Songs",
    fill = "Recommender"
  ) +
  theme(
    axis.text = element_text(size = 24), # Adjust axis labels
    axis.title = element_text(size = 24), # Adjust axis titles
    plot.title = element_text(size = 24),  # Adjust plot title
    legend.text = element_text(size = 18),  # Adjust legend text
    legend.title = element_text(size = 20), # Adjust legend titleMetronidazole
    strip.text.x = element_text(size = 20)
  )  

fft_data <- read.csv("data\\fft_for_each_song_id.csv")

fake_otu_table <-fft_data %>%
  column_to_rownames("X") %>% 
  mutate(across(everything(), as.numeric)) %>%
  rownames_to_column("song_id") %>% 
  pivot_longer(!song_id, names_to = "Freq", values_to = "Abundance") %>%
  group_by(song_id) %>%
  mutate(Abundance = Abundance/sum(Abundance)) %>%
  ungroup() %>%
  pivot_wider(names_from = "song_id", values_from = "Abundance") %>% 
  mutate(Freq = stringr::str_replace(Freq, "X", "")) %>% 
  column_to_rownames("Freq") %>% 
  otu_table(taxa_are_rows = T) 

fake_sample_data <- song_data %>%
  filter(song_id %in% colnames(fake_otu_table)) %>%
  column_to_rownames("song_id") %>% 
  sample_data()

fake_phyloseq <- phyloseq(fake_otu_table, fake_sample_data)

phy_ord = ordinate(fake_phyloseq, "PCoA", "bray")
pcoa_plt = plot_ordination(fake_phyloseq, phy_ord, 
                           type="samples",
                           color = "recommender_factor") +
  theme_classic() + 
  geom_point(size=6) +
  labs(
    title = "Comp Micro Music Taste PCOA",
    color = "Recommender") +
  theme(panel.border = element_rect(colour = "black", fill=NA, size=1)) + 
  theme(
    axis.text.x=element_blank(),
    axis.ticks.x=element_blank(),
    axis.text.y=element_blank(),
    axis.ticks.y=element_blank()
  ) +
  geom_text(aes(label = song_title), vjust = -1, hjust = 0.5, size = 3) +
  theme(
    axis.text = element_text(size = 24), # Adjust axis labels
    axis.title = element_text(size = 24), # Adjust axis titles
    plot.title = element_text(size = 24),  # Adjust plot title
    legend.text = element_text(size = 18),  # Adjust legend text
    legend.title = element_text(size = 20), # Adjust legend titleMetronidazole
    strip.text.x = element_text(size = 20)
  )  
print(pcoa_plt)

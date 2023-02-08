# list of packages needed
wants <- c("openxlsx",
           "stringr")
has <- wants %in% rownames(installed.packages())
if(any(!has)) install.packages(wants[!has])
lapply(wants, require, character.only = TRUE)

# homeoffice path
# path = 'C:/Users/monar/Google Drive/Arbeit/homeoffice/230103_RH review/barr1+2 interactome/stringDB_data/GO_analysis/'
# IMZ path
path <- 'B:/FuL/IMZ01/Hoffmann/Personal data folders/Mona/Paper/XXX_Haider et al_Review/barr1+2 interactome/stringDB_data/GO_analysis/'
setwd(path)

import_xlsx <- function(filename_pattern) {
  file_names = list.files(pattern = "*.xlsx", full.names = TRUE)
  file_names <- file_names[which(str_detect(file_names, filename_pattern))]

  # e.g. with GPCR or without
  conditions <- substr(file_names, 3, nchar(file_names) - 5)
  data <- vector("list")
  i = 1
  for (file in substr(file_names, 1, nchar(file_names))) {
    data[[conditions[i]]] <- read.xlsx(file)
    i = i + 1
  }
  return(data)
}

data_list <- import_xlsx('GO')



test_data <- data_list[[1]]

# count certain GO
ba1_freq <- table(as.factor(a1[,"GO_ids"]))
ba2_freq <- table(as.factor(a2[,"GO_ids"]))
# pseudo code
freq_df <- data.frame(GO_ids = levels(as.factor(test_data[,"GO_ids"])))
ba1_col<- c()
ba2_col <- c()
# for each level in as.factor(test_data[,"GO_ids"])
# ba1_col <- ba1_freq[level]
# ba2_col <- ba2_freq[level]
# if NA, return 0 # -> wrap this in a function
# add bar1_col and ba2_col as new cols to freq_df

# then use this df to create matrices for each ID in a loop
# non-ID counts via -->
# length(levels(as.factor(a1[,"uniprot_ID_proteinB"]))) - ID_counts
# (first part above is count of unique proteins in a1

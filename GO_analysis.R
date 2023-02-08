# list of packages needed
wants <- c("openxlsx",
           "stringr")
has   <- wants %in% rownames(installed.packages())
if(any(!has)) install.packages(wants[!has])
lapply(wants, require, character.only = TRUE)

# homeoffice path
# path = 'C:/Users/monar/Google Drive/Arbeit/homeoffice/230103_RH review/barr1+2 interactome/stringDB_data/GO_analysis/'
# IMZ path
path <- 'B:/FuL/IMZ01/Hoffmann/Personal data folders/Mona/Paper/XXX_Haider et al_Review/barr1+2 interactome/stringDB_data/GO_analysis/'
setwd(path)

##### import data #####
file_names = list.files(pattern="*.xlsx", full.names = TRUE)
file_names <- file_names[which(str_detect(file_names, "GO"))]

# e.g. with GPCR or without
conditions <- substr(file_names, 3, nchar(file_names)-5)

data <- vector("list")
i = 1
for (file in substr(file_names, 1, nchar(file_names))){
  data[[conditions[i]]] <- read.xlsx(file)
  i = i +1
}

### environment ###
# list of packages needed
wants <- c("simplifyEnrichment",
           "stringr")
has <- wants %in% rownames(installed.packages())
if(any(!has)) install.packages(wants[!has])
lapply(wants, require, character.only = TRUE)


### functions ###

# in chart table second column "Term" has GO IDs and text
# -> ID has to be extracted using following function
get_GO_id <- function(GO_id){
  ID <- str_extract_all(GO_id,".*~")[[1]]
  ID <- str_remove(ID, "~")
  return(ID)
}

# function to prepare each chart for analysis/visualization
format_chart <- function(chart){
  formatted <- chart
  formatted$ID <- lapply(chart[,2], get_GO_id)
  return(formatted)
}

### paths and import ###
# homeoffice path
# path =
# IMZ path
path <- r"(B:\FuL\IMZ01\Hoffmann\Personal data folders\Mona\Paper\XXX_Haider et al_Review\barr1+2 interactome\230227_PPI_analysis\after talking to Dario\Datasets\without GPCRs)"
subpath <- r"(\only biological process annot)"

setwd(paste0(path, subpath))

# import annotation charts which contain enriched GO terms
filenames <- list.files(getwd(), pattern = "chart.txt")

chart_list <- list()
for(file in filenames){
  chart_list[[file]] <- read.delim(file, header = TRUE)
  chart_list[[file]] <- format_chart(chart_list[[file]])
}




# GO terms have to be spearated first! at ~, use stringr package to create new col
t <- read.delim(filenames[1])
t[2]
names(t)
t$ID <- lapply(t[,2], get_GO_id)
names(t)

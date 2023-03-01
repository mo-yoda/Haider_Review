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
  formatted$ID <- unlist(lapply(chart[,2], get_GO_id))
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

### simplifyEnrichment ###
# plot similiarty matrix for one enrichment analysis

workflow_single <- function(GO_id){
  # create similiarity matrix
  sim_matrix = GO_similarity(GO_id)
  # cluster GO terms and create plot
  df = simplifyGO(sim_matrix)
}

# for bArr1 only with all GO terms in chart export from DAVID
workflow_single(chart_list[[1]]$ID)

# for bArr2 only with all GO terms in chart export from DAVID
workflow_single(chart_list[[2]]$ID)

# subset to only use GO_ids with an EASE score (more conservative p value) < 0.05
sig_list <- list()
for(file in names(chart_list)){
  temp_df <- chart_list[[file]]
  df_sub <- temp_df[temp_df$PValue < 0.05, ]
  sig_list[[file]] <- df_sub
}

# run workflow with this subset
# bArr1
workflow_single(sig_list[[1]]$ID)
# bArr2
workflow_single(sig_list[[2]]$ID)




# GO terms have to be spearated first! at ~, use stringr package to create new col
t <- read.delim(filenames[1])
t[2]
names(t)
t$ID <- unlist(lapply(t[,2], get_GO_id))
names(t)
hist(t$PValue)



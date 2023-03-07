### environment ###
# list of packages needed
wants <- c("simplifyEnrichment",
           "stringr",
           "openxlsx")
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
path <- r"(B:\FuL\IMZ01\Hoffmann\Personal data folders\Mona\Paper\XXX_Haider et al_Review\barr1+2 interactome\230227_PPI_analysis_THIS\after talking to Dario_THIS\without GPCRs)"
# enr_background <- r"(\enrichment specific against all interactors)"
enr_background <- r"(\enr specific against all interactors)"
subpath <- r"(\only biological process annot)"

setwd(paste0(path, enr_background, subpath))

# import annotation charts (exported from DAVID) which contain enriched GO terms
filenames <- list.files(getwd(), pattern = "chart.txt")
print(filenames)

chart_list <- list()
for(file in filenames){
  chart_list[[file]] <- read.delim(file, header = TRUE)
  chart_list[[file]] <- format_chart(chart_list[[file]])
}

### simplifyEnrichment - explore datesets ###
# plot similiarty matrix for one enrichment analysis

workflow_single <- function(GO_id){
  # create similiarity matrix
  sim_matrix = GO_similarity(GO_id)
  # cluster GO terms and create plot using >binary cutoff<
  df = simplifyGO(sim_matrix)
}

# for bArr1 only with all GO terms in chart export from DAVID
workflow_single(chart_list[[1]]$ID)

# for bArr2 only with all GO terms in chart export from DAVID
workflow_single(chart_list[[2]]$ID)

# for "both" interactors with all GO terms in chart export from DAVID
workflow_single(chart_list[[3]]$ID)

# subset to only use GO_ids with an EASE score (more conservative p value) < 0.05
sig_list <- list()
for(file in names(chart_list)){
  temp_df <- chart_list[[file]]
  # PValue = EASE score
  df_sub <- temp_df[temp_df$PValue < 0.05, ]
  sig_list[[file]] <- df_sub
}

# run workflow with this subset
# bArr1
workflow_single(sig_list[[1]]$ID)
# bArr2
workflow_single(sig_list[[2]]$ID)

### multiple lists of GO terms ###
# first, use subsetted GO_ids (EASE score < 0.05)
sig_GOs_list <- list()
sig_GOs_list[["bArr1"]] <- c(sig_list[[1]]$ID)
sig_GOs_list[["bArr2"]] <- c(sig_list[[2]]$ID)
simplifyGOFromMultipleLists(sig_GOs_list)

# run with all GO_ids (EASE score < 0.1)
GOs_list <- list()
GOs_list[["bArr1"]] <- c(chart_list[[1]]$ID)
GOs_list[["bArr2"]] <- c(chart_list[[2]]$ID)
# GOs_list[["both"]] <- c(chart_list[[3]]$ID)
simplifyGOFromMultipleLists(GOs_list)

### improve heatmap display ###
simplifyGOFromMultipleLists(sig_GOs_list)



### get details from clustering ###
GO_clusters <- simplifyGOFromMultipleLists(sig_GOs_list, plot = FALSE)

# get cluster of placement of each GO term
# add column to initial data which holds the cluster in which this GO term was clustered
GO_in_clusters_list <- list()
i = 1
for (df in chart_list){
  cluster_of_GO <- c()
  df_sub <- df[df$PValue < 0.05, ]
  for (GO in df_sub$ID){
    temp_cluster <- GO_clusters$cluster[GO_clusters$id == GO]
    if(length(temp_cluster) == 0){
      temp_cluster <- "NA"
    }
    cluster_of_GO <- c(cluster_of_GO, temp_cluster)
  }
  df_sub$cluster <- cluster_of_GO
  GO_in_clusters_list[[i]] <- df_sub
  i = i+1
}

# get proteins which are represented in clusters via GO term
get_ids_per_cluster <- function(df){
  proteins_in_clusters_list <- list()
    for (cluster in levels(as.factor(df$cluster))){
    print("---------------")
    print(cluster)
    # get uniprot IDs per cluster
    temp_uni_ids <- t$Genes[t$cluster == cluster]
    # as they are sorted per GO term, split + unlist to get one vector per cluster
    temp_uni_ids <- str_split(temp_uni_ids, ", ")
    temp_uni_ids <- unlist(temp_uni_ids)
    # remove duplicates
    temp_uni_ids <- unique(temp_uni_ids)
    proteins_in_clusters_list[[cluster]] <- unlist(temp_uni_ids)
  }
  return(proteins_in_clusters_list)
}
proteins_in_clusters_bArr1 <- get_ids_per_cluster(GO_in_clusters_list[[1]])
proteins_in_clusters_bArr2 <- get_ids_per_cluster(GO_in_clusters_list[[2]])

# export details from clustering
path_to_results = r"(B:\FuL\IMZ01\Hoffmann\Personal data folders\Mona\Paper\XXX_Haider et al_Review\barr1+2 interactome\230307_cluster_details)"
setwd(path_to_results)
write.xlsx(proteins_in_clusters_bArr1, file = "proteins_in_clusters_bArr1.xlsx")
write.xlsx(proteins_in_clusters_bArr2, file = "proteins_in_clusters_bArr2.xlsx")
names(GO_in_clusters_list) <- c("bArr1", "bArr2", "both")
write.xlsx(GO_in_clusters_list, file = "GO_in_clusters_list.xlsx")


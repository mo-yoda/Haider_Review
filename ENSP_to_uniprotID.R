# OmnipathR package is used
wants <- c("OmnipathR",
           "openxlsx",
           "stringr")
has <- wants %in% rownames(installed.packages())
if (any(!has)) install.packages(wants[!has])
lapply(wants, require, character.only = TRUE)

# homeoffice path
# path <- 'C:/Users/monar/Google Drive/Arbeit/homeoffice/230103_RH review/barr1+2 interactome/stringDB_data/'
# IMZ path
path <- 'B:/FuL/IMZ01/Hoffmann/Personal data folders/Mona/Paper/XXX_Haider et al_Review/barr1+2 interactome/stringDB_data/'
setwd(path)

# import xlsx, created by reformat_stringPPIdf.py
filenames <- list.files(path, pattern = ".xlsx")

df_list <- list()
for (file in filenames) {
  # import all xlsx files in path
  df_list[[str_remove(file, ".xlsx")]] <- read.xlsx(file)
}
names(df_list)

# translates ensp in uniprot IDs and adds this as new col to df
ensp_to_id <- function(df, ensp_col){
  # create temporary col with ensp without first 5x characters
  df$temp <- sapply(df[ensp_col], str_sub, 6)
  # translate these ensp to uniprot IDs
  df <- translate_ids(df, temp = ensp, uniprot)
  # remove temporary col
  df_edited <- subset(df, select=-c(temp))
  return(df_edited)
}

# use created function on every xlsx dataset in list and create list of result dfs
result_list <- list()
for (dataset in names(df_list)){
  print(dataset)
  result_list[[dataset]] <- ensp_to_id(df_list[[dataset]], "stringId_B")
}

# export all datasets created with filename extension "_ID"
for (dataset in names(result_list)){
  write.xlsx(result_list[[dataset]], paste0(path, "/uniprot_ID/", dataset, "_ID.xlsx"))
}

# unclear why some ENSP cannot be translated to uniprot IDs

# example where id is missing: 9606.ENSP00000351805	AVPR2
# it works with: 9606.ENSP00000337383	NLRP3
x <- data.frame("ensp" = c("ENSP00000351805", "ENSP00000337383"))
translate_ids(x, ensp = ensp, hgnc, uploadlists = TRUE)
uniprot_full_id_mapping_table(uniprot, ensg)

# at least get indices of non-assigned ENSP -> to many to assign manually
which(is.na(result_list[[1]]$uniprot))

y <- data.frame(protein_name = c("AVPR2", "NLRP3"))

translate_ids(y, protein_name = protein_name, id)

# USE uniprot maaping tool, is there API access?
# STRING has to be selected as input! -> only then, ENSP is specific!
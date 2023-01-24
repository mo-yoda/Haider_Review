# OmnipathR package is used
wants <- c("OmnipathR")
has   <- wants %in% rownames(installed.packages())
if(any(!has)) install.packages(wants[!has])
lapply(wants, require, character.only = TRUE)

# homeoffice path
# path <- 'C:/Users/monar/Google Drive/Arbeit/homeoffice/230103_RH review/barr1+2 interactome/stringDB_data/'
# IMZ path
path <- 'B:/FuL/IMZ01/Hoffmann/Personal data folders/Mona/Paper/XXX_Haider et al_Review/barr1+2 interactome/stringDB_data/'

# continue here! unfinished script



### following works --> write in beautiful
library(OmnipathR)

# ACHTUNG here erst ab ENSP als input, dann gehts!!!
c <- data.frame(ensp = c('ENSP00000409581', 'ENSP00000403701'))

e <- translate_ids(c, ensp = ensp, uniprot)
e
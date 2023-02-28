# list of packages needed
wants <- c("stringr")
has <- wants %in% rownames(installed.packages())
if(any(!has)) install.packages(wants[!has])
lapply(wants, require, character.only = TRUE)

# homeoffice path
# path =
# IMZ path
path <- r"(B:\FuL\IMZ01\Hoffmann\Personal data folders\Mona\Paper\XXX_Haider et al_Review\barr1+2 interactome\230227_PPI_analysis\after talking to Dario\Datasets\without GPCRs)"
setwd(path)
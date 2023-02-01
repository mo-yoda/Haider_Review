import os
import pandas as pd
import requests
import io

# homeoffice path
# path = 'C:/Users/monar/Google Drive/Arbeit/homeoffice/230103_RH review/barr1+2 interactome/stringDB_data/'
# IMZ path
path = 'B:/FuL/IMZ01/Hoffmann/Personal data folders/Mona/Paper/XXX_Haider et al_Review/barr1+2 interactome/stringDB_data/'

# HELP
# https://string-db.org/help/api/

# what we need:
# /api/tsv/interaction_partners? -> Gets all the STRING interaction partners of your proteins


# api parameters, see help site for options
string_api_url = "https://string-db.org/api"
output_format = "tsv"
method = "interaction_partners"

# get STRING ENS via uniprot (manually)
# bArr1 9606.ENSP00000409581
# bArr2 9606.ENSP00000403701
my_genes = ["9606.ENSP00000409581", "9606.ENSP00000403701"]

# built request api
# https://string-db.org/api/[output-format]/interaction_partners?identifiers=[your_identifiers]&[optional_parameters]
request_url = "/".join([string_api_url, output_format, method])
print(request_url)

# set parameters for request
params = {
    "identifiers": "%0d".join(my_genes),
    "species": 9606,  # species NCBI identifier for human
    "limit": 1000,  # limits the number of interaction proteins retrieved per protein
    "caller_identity": "Mona"  # my identifier for stringDB
}

# call STRING request
response = requests.post(request_url, data=params)

# Read and parse the results
# see help for all option of scores which can be retrieved
temp_row = str()
data_string = str()
for line in response.text.strip().split("\n"):
    l = line.strip().split("\t")
    query_ensp = l[0]
    query_name = l[2]
    partner_ensp = l[1]
    partner_name = l[3]
    combined_score = l[5]  # in help called "score"
    text_score = l[12]  # textmining score (aus interesse)
    temp_row = "\t".join([query_ensp, query_name,
                          partner_ensp, partner_name,
                          combined_score, text_score])
    data_string += temp_row + "\n"

# string to dataframe
df = pd.read_csv(io.StringIO(data_string), sep="\t")

# make new folder, if is not there yet
try:
    os.mkdir(path + "/OG_stringDB_data/")
except FileExistsError:
    pass
df.to_excel(path + "/OG_stringDB_data/" + "interactors_stringDB.xlsx")

##  about the combined_score
# The combined score is computed by combining the probabilities from the different evidence channels and
# corrected for the probability of randomly observing an interaction. For a more detailed description please
# see von Mering, et al. Nucleic Acids Res. 2005

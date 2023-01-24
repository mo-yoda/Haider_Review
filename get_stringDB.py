import xml.etree.ElementTree as ET
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
#/api/tsv/interaction_partners? -> Gets all the STRING interaction partners of your proteins


# api parameters, see help site for options
string_api_url = "https://string-db.org/api"
output_format = "tsv"
method = "interaction_partners"

# get STRING ENS via uniprot
# bArr1 9606.ENSP00000409581
# bArr2 9606.ENSP00000403701
my_genes = ["9606.ENSP00000409581", "9606.ENSP00000403701"]

# built request api
# https://string-db.org/api/[output-format]/interaction_partners?identifiers=[your_identifiers]&[optional_parameters]
request_url = "/".join([string_api_url, output_format, method])
print(request_url)

# set parameters for request
params = {
    "identifiers" : "%0d".join(my_genes),
    "species" : 9606, # species NCBI identifier for human
    "limit" : 1000, # limits the number of interaction proteins retrieved per protein
    "caller_identity" : "Mona" # my identifier for stringDB
}

# call STRING request
response = requests.post(request_url, data = params)

# Read and parse the results
for line in response.text.strip().split("\n"):
    l = line.strip().split("\t")
    query_ensp = l[0]
    query_name = l[2]
    partner_ensp = l[1]
    partner_name = l[3]
    combined_score = l[5]
    print("\t".join([query_ensp, query_name, partner_name, combined_score]))


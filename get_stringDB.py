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






# # selected keywords to extract (only ones in category biological process + molecular function)
# def get_rest_api(api_url):
#     call = requests.get(api_url, headers={'Accept-Encoding': 'gzip'})
#     # Check the response status code
#     if call.status_code == 200:
#         # Extract the content of the response
#         content = call.content
#         # Decompress the content using gzip
#         decompressed_content = gzip.decompress(content)
#         # Convert the decompressed content to a string
#         data = decompressed_content.decode('utf-8')
#         # string to dataframe
#         df = pd.read_csv(io.StringIO(data), sep="\t")
#         return df
#


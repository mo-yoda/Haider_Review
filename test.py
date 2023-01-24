import requests

# def get_gene_name(accession_number):
#     # Send a GET request to the UniProt API
#     url = "https://www.uniprot.org/uniprot/" + accession_number + ".xml"
#     r = requests.get(url)
#     xml_data = r.text
#
#     # Parse the XML data
#     import xml.etree.ElementTree as ET
#     root = ET.fromstring(xml_data)
#     print(xml_data)
#
#     # Find the gene name
#     for entry in root.findall('./entry'):
#         for name in entry.findall('./gene/name'):
#             return name.text
#
# # Test the function
# accession_number = "P05771" #PKC beta
# gene_name = get_gene_name(accession_number)
# print(gene_name)


## test IdMappingClient
from unipressed import IdMappingClient
import time

request = IdMappingClient.submit(
     source="UniProtKB_AC-ID", dest="Gene_Name", ids={"A1L190"}
 )
time.sleep(1)
print(list(request.each_result()))

# which string for "source" is correct for ENSP?!
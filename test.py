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


# test running .R in python
# import subprocess
#
# path_Rscript = "C:/Users/M02847/AppData/Local/Programs/R/R-4.2.1/bin/Rscript.exe"
# path_R_file = "/Users/M02847/Desktop/test.R"
# input = "/Users/M02847/Desktop/test.xlsx"
#
# cmd = path_Rscript + " " + path_R_file + " " + input
# print(cmd)
# # res = subprocess.call("C:/Users/M02847/AppData/Local/Programs/R/R-4.2.1/bin/Rscript.exe /Users/M02847/Desktop/test.R", shell=True)
# # res
#
# test = subprocess.call(cmd, shell=True)
# test

print(range(3))
for i in range(3):
    print(i)
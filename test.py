# import requests

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

# # test creating dir, if dir is not there
# import os
# path = 'C:/Users/monar/Google Drive/Arbeit/homeoffice/230103_RH review/barr1+2 interactome/stringDB_data/'
# try:
#     os.mkdir(path + "/OG_stringDB_data/")
# except FileExistsError:
#     print("already there")
#     pass
# import xlrd
# xlrd.xlsx.ensure_elementtree_imported(False, None)
# xlrd.xlsx.Element_has_iter = True
#
# import pandas as pd
# # homeoffice path
# path = 'C:/Users/monar/Google Drive/Arbeit/homeoffice/230103_RH review/barr1+2 interactome/stringDB_data/OG_stringDB_data/'
# df = pd.read_excel(path + "interactors_stringDB.xlsx")
# print(df)

import pandas as pd

x = [1,1,1,1,12,3,3,4,5,6123,1,2,65,46,5,42,33,4,5,8,5,5]
a = [1,12,3,3,4,5]
C = list(set(x)-set(a))

# filter_set = set(a)
# C = [a for a in x if a not in filter_set]
print(C)
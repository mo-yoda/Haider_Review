import requests

def get_gene_name(accession_number):
    # Send a GET request to the UniProt API
    url = "https://www.uniprot.org/uniprot/" + accession_number + ".xml"
    r = requests.get(url)
    xml_data = r.text

    # Parse the XML data
    import xml.etree.ElementTree as ET
    root = ET.fromstring(xml_data)
    # print(xml_data)

    # # Find the gene name
    # for entry in root.findall('./entry'):
    #
    #     for name in entry.findall('./gene/name'):
    #         return name.text

    entry = root.find(add_uniprot_url('./entry'))
    # gene_name = get_info(entry, add_uniprot_url('./gene/name[@type="primary"]'))


    # print(get_info(entry, add_uniprot_url('./dbReference[@type = "GO"]')))
    # print(get_info(entry, add_uniprot_url('./dbReference/property[@type = "term"]')))
    x = str(get_info(entry, add_uniprot_url('./dbReference/property[@type = "term"]')))
    print(len(x))

    return x


def get_info(entry, xml_path):
    # if there is no entry, e.g. no ecNumber since protein is not an enzyme
    if not entry.findall(xml_path):
        # print("no attribute found")
        extracted_info = float("NaN")
    else:
        extracted_info = str()
        for info in entry.findall(xml_path):
            extracted_info += ", " + info.get('value')
            # print(info.get('value'))
    return extracted_info

def add_uniprot_url(xml_path):
    long_path = xml_path.replace("/", "/{http://uniprot.org/uniprot}")
    return long_path


# Test the function
accession_number = "P05771" #PKC beta
gene_name = get_gene_name(accession_number)
print(gene_name)

# gene_name = get_info(entry, add_uniprot_url('./gene/name[@type="primary"]'))




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

# import pandas as pd
#
# x = [1,1,1,1,12,3,3,4,5,6123,1,2,65,46,5,42,33,4,5,8,5,5]
# a = [1,12,3,3,4,5]
# C = list(set(x)-set(a))
#
# # filter_set = set(a)
# # C = [a for a in x if a not in filter_set]
# # print(C)
#
#
# # translation_df[translation_df["ENSP"] == ENSP]["ID"]
#
# df = pd.DataFrame([a,a])
# df.rename(columns = {0: "X"}, inplace=True)
# df.rename(columns = {1: "Y"}, inplace=True)
# print(df)
#
# print(df[df["X"] == 1]["Y"])
# print(df[df["X"] == 0]["Y"])
#
# d = df[df["X"] == 0]["Y"]
# print(len(d))
#
# import pandas as pd
#
# a = [float("NaN"),12,3,3,4,5]
# b = [4,5,6,7,8,3]
# df = pd.DataFrame([a,b])
# df.rename(columns = {0: "X"}, inplace=True)
# print(df)
#
# print("index of X == NA")
# print(df[df["X"]==float("NaN")].index)
#
# df = df.dropna(axis = 'index')
# print("dropped row df")
# print(df)
#
# import pandas as pd
#
# a = [float("NaN"),12,3,3,4,5]
# b = [4,5,6,7,8,3]
# df = pd.DataFrame([a,b])
# print(df)
# print(df[range(3,5)])
# print(len(df.columns))
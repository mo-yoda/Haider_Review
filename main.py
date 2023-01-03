import requests
import openpyxl
import xml.etree.ElementTree as ET
import pandas as pd

path = 'C:/Users/monar/Google Drive/Arbeit/homeoffice/230103_RH review/barr1+2 interactome/python_test/'
file = "access.xlsx"
column = "ID"


# function to import xlsx file with accession numbers
def uniprotList(path, file, column):
    df = pd.read_excel(io=path + file, engine="openpyxl")
    ID_list = df[column]
    return (ID_list)

# function to get information from a list of accession numbers
def get_all_info(ID_list):
    info_dic = {} # dictionary does not work --> evtl. anders abspeichern! list zu namen in dic fuunktioniert nicth; "title": [] ist dafuer noetig
    # anderer weg zum abspeichern der unterschiedlichen Infos finden
    print(info_dic)
    for ID in ID_list:
        print(import_xml(ID))
        info_dic[ID].append = [import_xml(ID)]



# test wie infos pro accession number abgespeichert werden koennen
x = {"PEIGF": [], "Pdsfg": [], "Psdfg": []}
x["PEIGF"].append(["0h65jk", 123])
print(x)


# function to import xml data
def import_xml(accession_number):
    url = "https://www.uniprot.org/uniprot/" + accession_number + ".xml"
    r = requests.get(url)
    xml_data = r.text

    # Parse the XML data
    root = ET.fromstring(xml_data)

    # Find the entry element
    entry_element = root.find('./{http://uniprot.org/uniprot}entry')

    gene_name = get_gene_name(entry_element)
    add_info = "dummy"

    return ([gene_name, add_info])


# function to find gene_name in entry
def get_gene_name(entry_element):
    for name in entry_element.findall(
            './{http://uniprot.org/uniprot}gene/{http://uniprot.org/uniprot}name[@type="primary"]'):
        primary_gene_name = name.text
        return (primary_gene_name)

# Test the function
# accession_number = "P49407"
# test = import_xml(accession_number)

# print(test)


# test
ID_list = uniprotList(path, file, column)
test2 = get_all_info(ID_list)
print(test2)


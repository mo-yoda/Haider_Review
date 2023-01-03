import requests
import openpyxl
import xml.etree.ElementTree as ET
import pandas as pd

path = 'C:/Users/monar/Google Drive/Arbeit/homeoffice/230103_RH review/barr1+2 interactome/python_test/'
file = "access.xlsx"
column = "ID"



# function to import xlsx file with accession numbers
def uniprotList(path, file, column):
    df = pd.read_excel(io = path + file, engine = "openpyxl")
    ID_list = df[column]
    return (ID_list)



# function to get information from a list of accession numbers


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

    return (gene_name)


# function to find gene_name in entry
def get_gene_name(entry_element):
    for name in entry_element.findall(
            './{http://uniprot.org/uniprot}gene/{http://uniprot.org/uniprot}name[@type="primary"]'):
        primary_gene_name = name.text
        return (primary_gene_name)

# Test the function
#accession_number = "P49407"
#test = import_xml(accession_number)

#print(test)


# test
test2 = uniprotList(path, file, column)
print(test2)
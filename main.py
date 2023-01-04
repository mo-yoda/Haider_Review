import xml.etree.ElementTree as ET
import pandas as pd
import requests

path = 'C:/Users/monar/Google Drive/Arbeit/homeoffice/230103_RH review/barr1+2 interactome/python_test/'
file = "access.xlsx"
column = "ID"


# function to import xlsx file with accession numbers, returns all gathered infos
def uniprotList(path, file, column):
    df = pd.read_excel(io=path + file, engine="openpyxl")
    # list of accession numbers
    ID_list = df[column]
    result_df = get_all_info(ID_list)
    return (result_df)

# function to get information from a list of accession numbers
def get_all_info(ID_list):
    result_df = pd.DataFrame()
    for ID in ID_list:
        # adds all information gathered with import_xml to new column in result_df
        result_df[ID] = pd.Series(import_xml(ID), name = ID)
    # transpose df -> row per accession number and add column titels
    result_df = result_df.transpose()
    result_df = result_df.reset_index(level=0)
    result_df.columns = ["ID", "Gene Name", "Species", "dummy"] ### !!! edit this according to extracted info!
    return(result_df)



# function to import xml data
def import_xml(accession_number):
    url = "https://www.uniprot.org/uniprot/" + accession_number + ".xml"
    r = requests.get(url)
    xml_data = r.text

    # Parse the XML data
    root = ET.fromstring(xml_data)

    # Find the entry element
    entry_element = root.find('./{http://uniprot.org/uniprot}entry')

    # extract certain information, for each own function
    gene_name = get_gene_name(entry_element)
    species = get_species(entry_element)
    add_info = "dummy"

    return([gene_name, species, add_info])


# function to find gene_name in entry
def get_gene_name(entry_element):
    for name in entry_element.findall(
            './{http://uniprot.org/uniprot}gene/{http://uniprot.org/uniprot}name[@type="primary"]'):
        primary_gene_name = name.text
        return (primary_gene_name)


# function to find species in entry
def get_species(entry_element):
    for species in entry_element.findall(
            './{http://uniprot.org/uniprot}organism/{http://uniprot.org/uniprot}name[@type="scientific"]'):
        scientific_species = species.text
        return (scientific_species)

### TODO:
# ?? get GO terms (are a lot for one protein) -> see if there are online tools
# get poss. catalytic activity -> ecNumber --> if its present, it is an enzyme
# get Keywords (only "biological function")



# function to export result, main function
def export_xlsx(path, file, column):
    result_df = uniprotList(path, file, column)
    result_df.to_excel(path+file[:-5]+"_result.xlsx")
    print(result_df)
    return(print("Finished"))





#test2
export_xlsx(path, file, column)
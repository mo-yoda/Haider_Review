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
        result_df[ID] = pd.Series(import_xml(ID), name=ID)
    # transpose df -> row per accession number and add column titels
    result_df = result_df.transpose()
    result_df = result_df.reset_index(level=0)
    result_df.columns = ["ID", "Gene Name", "Species", "EC Number", "dummy"]  ### !!! edit this according to extracted info!
    return (result_df)


# function to import xml data
def import_xml(accession_number):
    url = "https://www.uniprot.org/uniprot/" + accession_number + ".xml"
    r = requests.get(url)
    xml_data = r.text

    # Parse the XML data
    root = ET.fromstring(xml_data)

    # Find the entry element
    entry = root.find(add_uniprot_url('./entry'))

    # extract certain information, based on path to xml
    gene_name = get_info(entry, add_uniprot_url('./gene/name[@type="primary"]'))
    species = get_info(entry, add_uniprot_url('./organism/name[@type="scientific"]'))
    ec_number = get_info(entry, add_uniprot_url('./protein/recommendedName/ecNumber'))
    add_info = "dummy"

    return ([gene_name, species, ec_number, add_info])

# function to add "{http://uniprot.org/uniprot}" to xml paths
def add_uniprot_url(path):
    long_path = path.replace("/", "/{http://uniprot.org/uniprot}")
    return(long_path)


# general function to get info from uniprot entry based to the given path
def get_info(entry, path):
    # if there is no entry, e.g. no ecNumber since protein is not an enzyme
    if not entry.findall(path):
        print("no attribute found")
        extracted_info = ["NA"]
    else:
        for info in entry.findall(path):
            print(info.text)
            extracted_info = info.text
    return extracted_info



### TODO:
# ?? get GO terms (are a lot for one protein) -> see if there are online tools
# get Keywords (only "biological function")


# function to export result, main function
def export_xlsx(path, file, column):
    result_df = uniprotList(path, file, column)
    result_df.to_excel(path + file[:-5] + "_result.xlsx")
    print(result_df)
    return (print("Finished"))


# test2
export_xlsx(path, file, column)

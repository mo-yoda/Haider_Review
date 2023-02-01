import xml.etree.ElementTree as ET
import pandas as pd
import requests
import gzip
import io
import os

# homeoffice path
path = 'C:/Users/monar/Google Drive/Arbeit/homeoffice/230103_RH review/barr1+2 interactome/stringDB_data/uniprot_ID/'
# IMZ path
# path = 'B:/FuL/IMZ01/Hoffmann/Personal data folders/Mona/Paper/XXX_Haider et al_Review/barr1+2 interactome/stringDB_data/uniprot_ID/'
file = "interactors_stringDB_ID.xlsx"
column = "uniprot_ID_proteinB"


# selected keywords to extract (only ones in category biological process + molecular function)
def get_rest_api(api_url):
    call = requests.get(api_url, headers={'Accept-Encoding': 'gzip'})
    # Check the response status code
    if call.status_code == 200:
        # Extract the content of the response
        content = call.content
        # Decompress the content using gzip
        decompressed_content = gzip.decompress(content)
        # Convert the decompressed content to a string
        data = decompressed_content.decode('utf-8')
        # string to dataframe
        df = pd.read_csv(io.StringIO(data), sep="\t")
        return df

# keyword API from uniprot
print("Getting Keywords from Uniprot ...")
keyword_url = "https://rest.uniprot.org/keywords/stream?compressed=true&fields=id%2Cname%2Ccategory%2Cgene_ontologies&format=tsv&query=%28%2A%29%20AND%20%28category%3A"
biol_processes = get_rest_api(keyword_url + "biological_process%29")
mol_function = get_rest_api(keyword_url + "molecular_function%29")
cell_comp = get_rest_api(keyword_url + "cellular_component%29")

# join both dfs + export
selected_keywords = pd.concat([biol_processes, mol_function, cell_comp])
selected_keywords.to_excel(path + "selected_keywords.xlsx")

# create list with Keyword IDs
kw_list = selected_keywords["Keyword ID"]


# function to import xlsx file with accession numbers, returns all gathered infos
def uniprotlist(path_to_folder, filename, column_name):
    print("Gathering info from Uniprot ...")
    df = pd.read_excel(io=path_to_folder + filename, engine="openpyxl")
    # list of accession numbers
    id_list = df[column_name]
    result_df = get_all_info(id_list)
    return result_df


# function to get information from a list of accession numbers
def get_all_info(id_list):
    result_df = pd.DataFrame()
    for ID in id_list:
        print(ID)
        # adds all information gathered with import_xml to new column in result_df
        # following line did work for small datasets, but gave performance warning for large dataset
        # result_df[ID] = pd.Series(import_xml(ID), name=ID)
        result_df = pd.concat((result_df, pd.Series(import_xml(ID), name=ID)), axis=1)
    # transpose df -> row per accession number and add column titles
    result_df = result_df.transpose()
    result_df = result_df.reset_index(level=0)
    result_df.columns = ["ID",
                         "Gene Name",
                         "Protein Name",
                         "Species",
                         "EC Number",
                         "Uniprot Keyword",
                         "dummy"]  # !!! edit this according to extracted info!
    return result_df


# function to import xml data for each accession number
def import_xml(accession_number, keyword_list=kw_list):
    url = "https://www.uniprot.org/uniprot/" + accession_number + ".xml"
    r = requests.get(url)
    xml_data = r.text

    # Parse the XML data
    root = ET.fromstring(xml_data)

    # Find the entry element
    entry = root.find(add_uniprot_url('./entry'))

    # extract certain information, based on path to xml
    gene_name = get_info(entry, add_uniprot_url('./gene/name[@type="primary"]'))
    protein_name = get_info(entry, add_uniprot_url('./protein/recommendedName/fullName'))
    species = get_info(entry, add_uniprot_url('./organism/name[@type="scientific"]'))
    ec_number = get_info(entry, add_uniprot_url('./protein/recommendedName/ecNumber'))

    # several keywords for each entry
    keywords = str()
    for key in keyword_list:  # extract only relevant ones according to kw_list
        temp = get_info(entry, add_uniprot_url('./keyword[@id="' + key + '"]'))
        # if there is an entry, add string to keywords
        if not pd.isna(temp):
            keywords = keywords + ", " + temp
    # remove first ", "
    keywords = keywords[2:len(keywords)]

    add_info = "dummy"
    return [gene_name, protein_name, species, ec_number, keywords, add_info]


# function to add "{http://uniprot.org/uniprot}" to xml paths
def add_uniprot_url(xml_path):
    long_path = xml_path.replace("/", "/{http://uniprot.org/uniprot}")
    return long_path


# general function to get info from uniprot entry based on the given path
def get_info(entry, xml_path):
    # if there is no entry, e.g. no ecNumber since protein is not an enzyme
    if not entry.findall(xml_path):
        # print("no attribute found")
        extracted_info = float("NaN")
    else:
        for info in entry.findall(xml_path):
            # print(info.text)
            extracted_info = info.text
    return extracted_info


# function to extract all rows containing a specific value in a specific column, used to identify GPCRs
def extract_rows(df, column, value):
    return df[(df[column].notnull()) & (df[column].str.contains(value))]

# removes rows from df when one of the values are found in specific column, used to remove GPCRs from "all"
def remove_rows(df, column, value):
    return df[(df[column].notnull()) & (df[column].str.contains(value)==False)]

# function to export result, main function
def export_xlsx(path_to_folder, filename, column_name):
    result_df = uniprotlist(path_to_folder, filename, column_name)
    print("Saving results ...")
    # split table into GPCR and non-GPCR proteins
    gpcr_df = extract_rows(result_df, 'Uniprot Keyword', 'G-protein coupled receptor')
    nogpcr_df = remove_rows(result_df, 'Uniprot Keyword', 'G-protein coupled receptor')

    try:
        os.mkdir(path + new_folder)
    except FileExistsError:
        pass
    result_df.to_excel(path_to_folder + new_folder + filename[:-5] + "_all.xlsx")
    gpcr_df.to_excel(path_to_folder + new_folder + filename[:-5] + "_gpcrs.xlsx")
    nogpcr_df.to_excel(path_to_folder + new_folder + filename[:-5] + "_nogpcrs.xlsx")
    return print("Finished")


# execute
export_xlsx(path, file, column)


# TODO
# add ENSP ID export to get_info()
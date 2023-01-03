import requests
import xml.etree.ElementTree as ET


# function to import xml data
def import_xml(accesssion_number):
    url = "https://www.uniprot.org/uniprot/" + accession_number + ".xml"
    r = requests.get(url)
    xml_data = r.text

    # Parse the XML data
    root = ET.fromstring(xml_data)

    # Find the entry element
    entry_element = root.find('./{http://uniprot.org/uniprot}entry')

    gene_name = get_gene_name(entry_element)

    return(gene_name)

# function to find gene_name in entry

def get_gene_name(entry_element):
    for name in entry_element.findall(
            './{http://uniprot.org/uniprot}gene/{http://uniprot.org/uniprot}name[@type="primary"]'):
        primary_gene_name = name.text
        return(primary_gene_name)




# Test the function
accession_number = "P49407"
test = import_xml(accession_number)

print(test)

import requests

def get_gene_name(accession_number):
    # Send a GET request to the UniProt API
    url = "https://www.uniprot.org/uniprot/" + accession_number + ".xml"
    r = requests.get(url)
    xml_data = r.text
    #print(xml_data)

    # Parse the XML data
    import xml.etree.ElementTree as ET
    root = ET.fromstring(xml_data)

    # Find the entry element
    entry_element = root.find('./{http://uniprot.org/uniprot}entry')

    # Find the primary gene name
    for name in entry_element.findall(
            './{http://uniprot.org/uniprot}gene/{http://uniprot.org/uniprot}name[@type="primary"]'):
        primary_gene_name = name.text
        return(primary_gene_name)

# Test the function
accession_number = "P49407"
gene_name = get_gene_name(accession_number)
print(gene_name)
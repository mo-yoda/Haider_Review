# Comparative Analysis of the Interactome of both β-Arrestin Isoforms
## Conformational flexibility of β-arrestins – how these scaffolding proteins guide and transform the functionality of GPCRs

Raphael Silvanus Haider*[1,2] ,  Mona Reichel*[1], Edda Sofie Fabienne Matthees[1], Carsten Hoffmann[1]

[1]: Institut für Molekulare Zellbiologie, CMB – Center for Molecular Biomedicine, Universitätsklinikum Jena, 
Friedrich-Schiller-Universität Jena, Hans-Knöll Straße 2, D-07745 Jena, Germany

[2]: Division of Physiology, Pharmacology and Neuroscience, School of Life Sciences, Queen's Medical Centre, 
University of Nottingham, Nottingham, UK

[*] contributed equally

---

**This code was written and used to perform the comparative interactome analysis of β-arrestin1 and 2 found in DOI.**

---

**Resource data**
- [interactors_stringDB_ID_gpcrs.xlsx](https://github.com/mo-yoda/Haider_Review/blob/master/interactors_stringDB_ID_gpcrs.xlsx)
- [interactors_stringDB_ID_nogpcrs.xlsx](https://github.com/mo-yoda/Haider_Review/blob/master/interactors_stringDB_ID_nogpcrs.xlsx)

**Details about enriched GO term clustering**
- [GO_in_clusters_list.xlsx](https://github.com/mo-yoda/Haider_Review/blob/master/GO_in_clusters_list.xlsx)
- [proteins_in_clusters_bArr1.xlsx](https://github.com/mo-yoda/Haider_Review/blob/master/proteins_in_clusters_bArr1.xlsx)
- [proteins_in_clusters_bArr2.xlsx](https://github.com/mo-yoda/Haider_Review/blob/master/proteins_in_clusters_bArr2.xlsx)

---
## Short description
Interacting proteins were retrieved from [STRINGdb 11.5](https://string-db.org/help/api/) 
[**(Szklarczyk et al. 2018)**](https://doi.org/10.1093/nar/gky1131). 
GO enrichment analysis was performed using the online tool 
[Database for Annotation, Visualization and Integrated Discovery (DAVID) 6.8](https://david.ncifcrf.gov/) 
[**(Huang et al. 2009**](https://doi.org/10.1038/nprot.2008.211), 
[**Sherman et al. 2022)**](https://doi.org/10.1093/nar/gkac194). 
Enriched GO terms were clustered and visualized using the [R/Bioconductor](https://www.bioconductor.org/) package 
[simplifyEnrichment](https://jokergoo.github.io/simplifyEnrichment/index.html) 
[**(Gu & Huebschmann 2022)**](https://doi.org/10.1016/j.gpb.2022.04.008).


---
## Workflow
### 1. Retrieving interacting proteins of β-arrestin1 and 2 from STRINGdb
#### [get_stringDB.py](https://github.com/mo-yoda/Haider_Review/blob/master/get_stringDB.py)
- retrieves all proteins interacting with β-arrestin1 or 2 from stringDB using 
[stringDB API](https://string-db.org/help/api/)
- entries with  confidence score < 0.5 are removed
- returns xlsx file with ENSP of interacting proteins, confidence score of this interaction and the "uniqueness" 
of the interaction (whether this interaction is unique to one of the β-arrestin isoforms)

#### [reformat_stringPPIdf.py](https://github.com/mo-yoda/Haider_Review/blob/master/reformat_stringPPIdf.py)
- splits xlsx file based on the "uniqueness" column
- returns xlsx files for β-arrestin1, β-arrestin2 and interactors of both isoforms

*(Note, that proteins interacting with both isoforms are found twice in these exports)*

---

### 2. Translating ENSP IDs to uniprot accession number
#### [ENSP_to_uniprotID.py](https://github.com/mo-yoda/Haider_Review/blob/master/ENSP_to_uniprotID.py)
- translates ENSP IDs exported from STRINGdb to uniprot accession number using the 
[uniprot ID mapping tool](https://www.uniprot.org/id-mapping) via
[the API](https://www.uniprot.org/help/id_mapping)
- *Note, that order of fetched IDs do not match order of requested IDs* - 
to prevent mistranslation, the script creates a translation dictionary which is then applied to the imported ENSP IDs
- returns input xlsx with additional column containing uniprot accession IDs

---

### 3. Extract information from uniprot entries
#### [extract_uniprot_info.py](https://github.com/mo-yoda/Haider_Review/blob/master/extract_uniprot_info.py)
- uniprot accession number duplicates in input table are removed (which are all proteins interacting with both 
β-arrestins as described above)
- using the uniprot accession number, selected information from each uniprot entry is retrieved via 
[APIs](https://www.uniprot.org/help/api_retrieve_entries) 
(*to test how certain information can be accessed from xml entry, test.xml was created*)
- according to the uniprot Keyword 'G-protein coupled receptor', resulting table is separated into interactors
which are GPCRs and non-GPCRs
  - these xlsx files are part of this repository:
  
    [interactors_stringDB_ID_gpcrs.xlsx](https://github.com/mo-yoda/Haider_Review/blob/master/interactors_stringDB_ID_gpcrs.xlsx), 
  [interactors_stringDB_ID_nogpcrs.xlsx](https://github.com/mo-yoda/Haider_Review/blob/master/interactors_stringDB_ID_nogpcrs.xlsx)


#### [GO_list.py](https://github.com/mo-yoda/Haider_Review/blob/master/GO_list.py)
*is unused for analysis, but gave an initial overview*
- retrieves GO terms of all three ontologies from uniprot using 
[APIs](https://www.uniprot.org/help/api_retrieve_entries) 
- lists each GO term separately with corresponding proteins

---

### 4. GO enrichment analysis via DAVID
GO enrichment analysis of the biological process ontology was performed using the online tool 
[DAVID 6.8](https://david.ncifcrf.gov/).
Uniprot accession numbers of non-GPCR proteins obtained from extract_uniprot_info.py were used as input.

In detail, functional annotation analysis was performed using the uniprot accession IDs of non-GPCR proteins
interacting with exclusively one β-arrestin isoform (gene list input) against all non-GPCR interacting proteins 
of this isoform (background).The functional annotation chart created by DAVID was downloaded and used in the last
step visualizeEnrichment.R.

---

### 5. Clustering and visualization of enriched GO terms
#### [visualizeEnrichment.R](https://github.com/mo-yoda/Haider_Review/blob/master/visualizeEnrichment.R)
- uses functional annotation chart created by [DAVID 6.8](https://david.ncifcrf.gov/) as input
- enriched GO terms for  β-arrestin1-only or  β-arrestin2-only interacting proteins are clustered according 
to their similarity and displayed as heatmap using `simplifyGOFromMultipleLists()` of the R/Bioconductor package 
[simplifyEnrichment](https://jokergoo.github.io/simplifyEnrichment/index.html) 
[**(Gu & Huebschmann 2022)**](https://doi.org/10.1016/j.gpb.2022.04.008)
- GO terms found in each cluster are exported as xlsx file 
  - part of this repository: [GO_in_clusters_list.xlsx](https://github.com/mo-yoda/Haider_Review/blob/master/GO_in_clusters_list.xlsx)
- additionally, proteins which contributed to each cluster due to their GO term assignment are exported as xlsx file 
  - these files are part of this repository: 
  [proteins_in_clusters_bArr1.xlsx](https://github.com/mo-yoda/Haider_Review/blob/master/proteins_in_clusters_bArr1.xlsx),
  [proteins_in_clusters_bArr2.xlsx](https://github.com/mo-yoda/Haider_Review/blob/master/proteins_in_clusters_bArr2.xlsx)
  
  (*Note, that one protein can contribute to several clusters as each protein has several GO terms assigned*)

---

This project is licensed under the terms of the MIT license.

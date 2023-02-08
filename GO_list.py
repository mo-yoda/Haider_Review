import pandas as pd

# homeoffice path
# path = 'C:/Users/monar/Google Drive/Arbeit/homeoffice/230103_RH review/barr1+2 interactome/stringDB_data/uniprot_details/'
# IMZ path
path = 'B:/FuL/IMZ01/Hoffmann/Personal data folders/Mona/Paper/XXX_Haider et al_Review/barr1+2 interactome/stringDB_data/uniprot_details/'
file = "interactors_stringDB_ID_nogpcrs.xlsx"

# import xlsx with all GO terms
df = pd.read_excel(io=path + file, engine="openpyxl")

# remove all rows with df["uniqueness"] == both
# bArr1 only vs bArr2 only will be tested
df.drop(df[df['uniqueness'] == 'both'].index, axis='index', inplace=True)

# subset table with needed cols
get_cols = [
    'preferredName_B',
    'uniqueness',
    'uniprot_ID_proteinB',
    'Gene Name',
    'Protein Name',
    'GO IDs',
    'GO terms']
df_sub = df[get_cols]



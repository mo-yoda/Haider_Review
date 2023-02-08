import pandas as pd

# homeoffice path
# path = 'C:/Users/monar/Google Drive/Arbeit/homeoffice/230103_RH review/barr1+2 interactome/stringDB_data/uniprot_details/'
# IMZ path
path = 'B:/FuL/IMZ01/Hoffmann/Personal data folders/Mona/Paper/XXX_Haider et al_Review/barr1+2 interactome/stringDB_data/uniprot_details/'
file = "interactors_stringDB_ID_nogpcrs.xlsx"

# function subset df to needed columns and factors
def format_df(df):
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
    return df_sub

# for each category get GO term and IDs
def get_category_id(GO_term_list, GO_id_list, category):
    # gets index of term of specific category
    indices = [id for id, i in enumerate(GO_term_list) if category in i]
    print(indices)
    print(len(GO_term_list))
    print(len(GO_id_list))
    GO_terms = []
    GO_ids = []
    # indices are then used to get the corresponding terms and ids
    for index in indices:
        print(index)
        print(GO_term_list[index])
        print(GO_id_list[index])
        GO_terms += [GO_term_list[index]]
        GO_ids += [GO_id_list[index]]
    return GO_terms, GO_ids

# create GO df for each category and
def GO_by_row(df):
     # each row represents one interaction protein
    for row in range(len(df)):
        print(row)
        print(df['preferredName_B'].iloc[row])
        temp_row = df.iloc[row]

        # split string to get single terms or ids
        GO_terms = str(temp_row['GO terms']).split(r'; ')
        GO_ids = str(temp_row['GO IDs']).split(r'; ')
        print(GO_terms)

        # get GO term and ids by category

        C_GO = get_category_id(GO_terms, GO_ids, 'C:')
        F_GO = get_category_id(GO_terms, GO_ids, 'F:')
        P_GO = get_category_id(GO_terms, GO_ids, 'P:')
    print("run successful")


def main(path_to_folder, filename):
    df = pd.read_excel(io=path_to_folder + filename, engine="openpyxl")
    df_sub = format_df(df)

    GO_by_row(df_sub)



main(path, file)










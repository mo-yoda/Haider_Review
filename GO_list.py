import pandas as pd
import os

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


# for each category get GO term and IDs, returns df
def get_category_id(GO_term_list, GO_id_list, category):
    # gets index of term of specific category
    indices = [id for id, i in enumerate(GO_term_list) if category in i]
    GO_terms = []
    GO_ids = []
    # this may be needed later?
    if len(indices) == 0:
        GO_terms = [float("NaN")]
        GO_ids = [float("NaN")]
    else:
        # indices are then used to get the corresponding terms and ids
        for index in indices:
            GO_terms += [GO_term_list[index]]
            GO_ids += [GO_id_list[index]]
    GO_df = pd.DataFrame({'GO_terms': GO_terms, 'GO_ids': GO_ids})
    return GO_df


def complete_category_df(df, row, category_df):
    n_rows = len(category_df)
    for cols in df.columns[0:len(df.columns) - 2]:
        value = df[cols].iloc[row]
        category_df = pd.concat((category_df,
                                 pd.Series([value] * n_rows).rename(cols)),
                                axis='columns')
    return category_df


def create_category_df(df, row, category):
    temp_row = df.iloc[row]

    # split string to get single terms or ids
    GO_terms = str(temp_row['GO terms']).split(r'; ')
    GO_ids = str(temp_row['GO IDs']).split(r'; ')

    category_df = get_category_id(GO_terms, GO_ids, category)
    category_df = complete_category_df(df, row, category_df)
    return category_df


# create GO df for each category and
def GO_by_row(df, category):
    print("Getting GOs for " + str(len(df)) + "x proteins")
    # initiate output df
    C_df = pd.DataFrame()

    # each row represents one interaction protein
    for row in range(len(df)):
        print(df['preferredName_B'].iloc[row])

        C_temp = create_category_df(df, row, category)
        C_df = pd.concat((C_df, C_temp), axis='index', ignore_index=True)
    return C_df


def main(path_to_folder, filename):
    df = pd.read_excel(io=path_to_folder + filename, engine="openpyxl")
    df_sub = format_df(df)
    print("Category: cellular component")
    C_GO = GO_by_row(df_sub, 'C:')
    print("Category: molecular function")
    F_GO = GO_by_row(df_sub, 'F:')
    print("Category: biological process")
    P_GO = GO_by_row(df_sub, 'P:')

    print("Exporting results...")
    new_folder = path_to_folder.replace("/uniprot_details/", "/GO_analysis/")
    try:
        os.mkdir(new_folder)
    except FileExistsError:
        pass
    C_GO.to_excel(new_folder + filename[:-5] + "_GO_C.xlsx")
    F_GO.to_excel(new_folder + filename[:-5] + "_GO_F.xlsx")
    P_GO.to_excel(new_folder + filename[:-5] + "_GO_P.xlsx")

    print("Finished")


main(path, file)

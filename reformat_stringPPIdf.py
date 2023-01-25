import pandas as pd

# import interactors retrieved from strinDB via get_stringDB.py
# homeoffice path
# path = 'C:/Users/monar/Google Drive/Arbeit/homeoffice/230103_RH review/barr1+2 interactome/stringDB_data/'
# IMZ path
path = 'B:/FuL/IMZ01/Hoffmann/Personal data folders/Mona/Paper/XXX_Haider et al_Review/barr1+2 interactome/stringDB_data/'

all_df = pd.read_excel(path + "interactors_stringDB.xlsx")
all_df.rename(columns = {all_df.columns[0]: "index"}, inplace=True)

## reformat retrieved interactors
# identify non-unique interactors, add columns with unique or non-unique
print(all_df.columns)
print(all_df.shape)

# index True for all duplicates, type is pd.Series
all_dupl = all_df.duplicated(subset="stringId_B", keep = False)

# create pd.Series for uniq/bArr1/bArr2
unique = []
for i, e in enumerate(all_dupl):
    if e: # means if e = True
        unique += ["both"]
    else:
        # add "bArr1" or "bArr2"
        unique += [all_df['preferredName_A'][i]]
unique = pd.Series(unique)


# add this series as new column to data
all_df_uniq = pd.concat([all_df, unique], axis = 1)
all_df_uniq.rename(columns = {0 : "uniqueness"}, inplace=True)
print(all_df_uniq)




# TODO
# add function to export bArr1, bArr2 interaction proteins separately

import pandas as pd

# import interactors retrieved from strinDB via get_stringDB.py
# homeoffice path
path = 'C:/Users/monar/Google Drive/Arbeit/homeoffice/230103_RH review/barr1+2 interactome/stringDB_data/'
# IMZ path
# path = 'B:/FuL/IMZ01/Hoffmann/Personal data folders/Mona/Paper/XXX_Haider et al_Review/barr1+2 interactome/stringDB_data/OG_stringDB_data/'

all_df = pd.read_excel(path + "interactors_stringDB.xlsx")
all_df.rename(columns={all_df.columns[0]: "index"}, inplace=True)

# reformat retrieved interactors

# export xlsx with all interactors
all_df_uniq.to_excel(path + "all_interactors.xlsx")

# create separate DFs based on "uniqueness" column
arrb1_only = all_df_uniq[all_df_uniq["uniqueness"] == "ARRB1"]
arrb2_only = all_df_uniq[all_df_uniq["uniqueness"] == "ARRB2"]
both_arrb = all_df_uniq[all_df_uniq["uniqueness"] == "both"]

# export all DFs
all_df_uniq.to_excel(path + "all_interactors.xlsx")
arrb1_only.to_excel(path + "ARRB1_interactors.xlsx")
arrb2_only.to_excel(path + "ARRB2_interactors.xlsx")
both_arrb.to_excel(path + "interactors_both_ARRB.xlsx")

# print dataset stats
print("-----------------------")
print("barr1 only interactors")
print(len(arrb1_only))
print("barr2 only interactors")
print(len(arrb2_only))

print("interactors of both barr")
print(len(both_arrb))

print("-----------------------")
print("barr1 interactors")
print(len(all_df[all_df["preferredName_A"] == "ARRB1"]))
print("barr2 interactors")
print(len(all_df[all_df["preferredName_A"] == "ARRB2"]))
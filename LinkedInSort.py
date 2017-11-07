import chardet
import pandas as pd
import numpy as np


def remove_empty_columns(df):
    flag = 0
    count = df.shape[1]
    # print(count)
    for i in range(count-1, 0, -1):
        for var in df[df.columns[i]][1:]:
            if pd.isnull(var):
                flag = 0
            else:
                flag = 1
                break

        if flag == 0:
            df.drop(df.columns[i], axis=1, inplace=True)
    return df


def remove_invalid_job_title(invalid, df):
    for i in range(len(invalid)):
        df.drop(df[df['Position'].str.lower() == invalid[i]].index, inplace=True)
        df.drop(df[df['Position'].str.contains(invalid[i]) == True].index, inplace=True)
    return df


def remove_invalid_comp(invalid, df):
    for i in range(len(invalid)):
        df.drop(df[df['Company'].str.lower() == invalid[i]].index, inplace=True)
        df.drop(df[df['Company'].str.contains(invalid[i]) == True].index, inplace=True)
    return df


def creat_invalid_list():
    F = open('invalid1.txt', 'r')
    f = F.read()
    invalid = f.split('\n')
    while True:
        if invalid[len(invalid)-1] == '':
            del invalid[-1]
        else:
            break
    return invalid


def get_deleted_df(df_orig, df_sorted):
	sorted_emails = df_sorted['Email Address']
	all_emails = df_orig['Email Address']
	deleted_emails = np.setdiff1d(all_emails, sorted_emails)
	df_deleted = df_orig[df_orig['Email Address'].isin(deleted_emails)]
	return df_deleted
	


# Reading Connections
with open('Connections.csv', 'rb') as f:
    result = chardet.detect(f.read())  # or readline if the file is large
df_orig = pd.read_csv('Connections.csv', encoding=result['encoding'])

# Making a copy of orignal
df_orig = pd.concat([df_orig[col].astype(str).str.lower() for col in df_orig.columns], axis=1)
df = df_orig.copy()
# df['index'] = df.index

# remove invalid rows
invalid = creat_invalid_list()
remove_invalid_job_title(invalid, df)
remove_invalid_comp(invalid, df)

# Getting the deleted Dataframe
df_deleted = get_deleted_df(df_orig, df)

# Saving data
print('\n\nAbout to save your data in sorted data.csv\n\n')
df.to_csv('sorted data.csv')
df_deleted.to_csv('deleted data.csv')
print('Done !!')

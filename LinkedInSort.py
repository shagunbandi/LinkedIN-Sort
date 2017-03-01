import chardet
import pandas as pd
import numpy as np

with open('data.csv', 'rb') as f:
    result = chardet.detect(f.read())  # or readline if the file is large


df = pd.read_csv('data.csv', encoding=result['encoding'])

def remove_empty_columns():
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


def remove_invalid_job_title():
    for i in range(len(invalid)):
        df.drop(df[df['Job Title'].str.lower() == invalid[i]].index, inplace=True)
        df.drop(df[df['Job Title'].str.contains(invalid[i]) == True].index, inplace=True)


def remove_invalid_comp():
    for i in range(len(invalid)):
        df.drop(df[df['Company'].str.lower() == invalid[i]].index, inplace=True)
        df.drop(df[df['Company'].str.contains(invalid[i]) == True].index, inplace=True)

invalid = ['nan']

def creat_invalid_list():
    F = open('invalid1.txt', 'r')
    f = F.read()
    global invalid
    invalid = f.split('\n')
    while 1==1:
        if invalid[len(invalid)-1] == '':
            del invalid[-1]
        else:
            break


remove_empty_columns()

df = pd.concat([df[col].astype(str).str.lower() for col in df.columns], axis=1)
creat_invalid_list()
remove_invalid_job_title()
remove_invalid_comp()

df.sort_values(by=['Company'], ascending=True, inplace=True)
df.set_index('First Name', inplace=True)

print(df.head())
print('\n\nAbout to save your data in final.csv\n\n')
df.to_csv('final.csv')
print('Done !!')

## Convert a standard The Lens csv to DSpace batch import format
## Anders Wändahl - anders@golonka.se

import pandas as pd
import numpy as np

df_lens = pd.read_csv("hej.csv", delimiter=',', quotechar='"', index_col=False, na_filter=False) ## import with nothing instead of NaN
#df_lens.insert(0, 'collection', '1/48935') ## create a new column to the left and fill it with the appropriate collection id
#df_lens.insert(0, 'id', '+') ## create a new column to the left and fill it with "+" = import of new records
df_lens = df_lens.astype(str)


#df_lens['Keywords'] = df_lens['Keywords'].replace({'\r\n': ''}, inplace=True, regex=True)
#df_lens['Fields of Study'] = df_lens['Fields of Study'].replace({'\r\n': ''}, inplace=True, regex=True)
#df_lens['MeSH Terms'] = df_lens['MeSH Terms'].replace({'\r\n': ''}, inplace=True, regex=True)
#df_lens['Chemicals'] = df_lens['Chemicals'].replace({'\r\n': ''}, inplace=True, regex=True)
#df_lens['Title'] = df_lens['Title'].replace({'\r\n': ''}, inplace=True, regex=True)
#df_lens['Abstract'] = df_lens['Abstract'].replace({'\r\n': ''}, inplace=True, regex=True)

#df_lens['Keywords'].replace({'a': '######### '}, inplace=True, regex=True)
#df_lens['Fields of Study'].replace({'\r\n': ' '}, inplace=True, regex=True)
#df_lens['MeSH Terms'].replace({'\r\n': ' '}, inplace=True, regex=True)
#df_lens['Chemicals'].replace({'\r\n': ' '}, inplace=True, regex=True)
#df_lens['hej'].str.replace({'\\r\\n': 'xx'}, regex=True)
df_lens['hej'] = df_lens['hej'].str.replace('\r\n','xx')

df_lens['hej'] = df_lens['hej'].str.strip('\\n')

#df_lens.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=[""&&&""], regex=True, inplace=True)



df_lens.to_csv(r'tt.csv', index=False)

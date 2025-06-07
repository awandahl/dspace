## Convert a standard Publish-or-Perish csv to DSpace batch import format
## Anders Wändahl - anders@golonka.se

import pandas as pd
#import numpy as np
df_pop_ma = pd.read_csv("pop_ma.csv", delimiter=',', index_col=False, na_filter=False) ## import with nothing instead of NaN
df_pop_ma.insert(0, 'from', 'ma') ## create a new column to the left and fill it with "ma" = Microsoft Academic
df_pop_cr = pd.read_csv("pop_cr.csv", delimiter=',', index_col=False, na_filter=False) ## import with nothing instead of NaN
df_pop_cr.insert(0, 'from', 'cr') ## create a new column to the left and fill it with "cr" = Crossref
df_pop_gs = pd.read_csv("pop_gs.csv", delimiter=',', index_col=False, na_filter=False) ## import with nothing instead of NaN
df_pop_gs.insert(0, 'from', 'gs') ## create a new column to the left and fill it with "gs" = Google Scholar

df_pop = pd.concat([df_pop_ma,df_pop_cr,df_pop_gs]) # concatenate the dfs above


df_pop.insert(0, 'collection', '1/48307') ## create a new column to the left and fill it with the appropriate collection id
df_pop.insert(0, 'id', '+') ## create a new column to the left and fill it with "+" = import of new records

## rename columns from pop tags to dc-metadata 
df_pop = df_pop.rename(columns={'Abstract': 'dc.description.abstract', 'Authors': 'dc.contributor.author', 'StartPage': 'dc.identifier.spage', 'DOI': 'dc.identifier.doi', 'Type': 'dc.type',  'EndPage': 'dc.identifier.epage', 'Issue': 'dc.identifier.issue', 'Publisher': 'dc.publisher', 'Year': 'dc.date.issued', 'ISSN': 'dc.identifier.issn', 'Source': 'dc.relation.ispartof', 'Title': 'dc.title', 'Volume': 'dc.identifier.volume'})

## drop all unused columns
df_pop.drop(['Cites','ArticleURL','CitesURL','GSRank','QueryDate','CitationURL','ECC','CitesPerYear','CitesPerAuthor','AuthorCount','Age'], 1, inplace=True)

## convert df to str
df_pop = df_pop.astype(str)

## replace , with ||
df_pop['dc.contributor.author'].replace({'\,': '||'}, inplace=True, regex=True)
df_pop['dc.identifier.doi'] = df_pop['dc.identifier.doi'].str.lower()

print(df_pop)

df_pop.to_csv(r'kyambogo_pop_out.csv', index=False)

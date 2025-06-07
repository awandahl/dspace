## Convert a standard Publish-or-Perish csv to DSpace batch import format
## Anders Wändahl - anders@golonka.se

import pandas as pd
import numpy as np
df_pop_cr = pd.read_csv("PoPCites_Crossref_Aff_Kyambogo.csv", delimiter=',', index_col=False, na_filter=False) ## import with nothing instead of NaN
df_pop_cr.insert(0, 'collection', '1/48307') ## create a new column to the left and fill it with the appropriate collection id
df_pop_cr.insert(0, 'id', '+') ## create a new column to the left and fill it with "+" = import of new records

## rename columns from WoS tags to dc-metadata 
df_pop_cr = df_pop_cr.rename(columns={'Abstract': 'dc.description.abstract', 'Authors': 'dc.contributor.author', 'StartPage': 'dc.identifier.spage', 'DOI': 'dc.identifier.doi', 'Type': 'dc.type',  'EndPage': 'dc.identifier.epage', 'Issue': 'dc.identifier.issue', 'Publisher': 'dc.publisher', 'Year': 'dc.date.issued', 'ISSN': 'dc.identifier.issn', 'Source': 'dc.relation.ispartof', 'Title': 'dc.title', 'Volume': 'dc.identifier.volume'})

## drop all unused columns
df_pop_cr.drop(['Cites','ArticleURL','CitesURL','GSRank','QueryDate','CitationURL','ECC','CitesPerYear','CitesPerAuthor','AuthorCount','Age'], 1, inplace=True)

## convert df to str
df_pop_cr = df_pop_cr.astype(str)

## replace , with ||
df_pop_cr['dc.contributor.author'].replace({'\,': '||'}, inplace=True, regex=True)
df_pop_cr['dc.identifier.doi'] = df_pop_cr['dc.identifier.doi'].str.lower()

print(df_pop_cr)

df_pop_cr.to_csv(r'pop_cr_out.csv', index=False)




## Convert a standard The Lens csv to DSpace batch import format
## Anders Wändahl - anders@golonka.se

import pandas as pd
import numpy as np
#df_lens = pd.read_csv("lens-export.csv", delimiter=',', index_col=False) ## import with NaN
df_lens = pd.read_csv("lens-export.csv", delimiter=',', index_col=False, na_filter=False) ## import with nothing instead of NaN
df_lens.insert(0, 'collection', '1/48935') ## create a new column to the left and fill it with the appropriate collection id
df_lens.insert(0, 'id', '+') ## create a new column to the left and fill it with "+" = import of new records


## rename columns from The Lens tags to dc-metadata 
df_lens = df_lens.rename(columns={
'Author/s': 'dc.contributor.author',
'Title': 'dc.title',
'Abstract': 'dc.description.abstract',
'Source Title': 'dc.relation.ispartof',
'ISSNs': 'dc.identifier.issn',
'Publication Type': 'dc.type',
'Volume': 'dc.identifier.volume',
'Issue Number': 'dc.identifier.issue',
'Start Page': 'dc.identifier.spage',
'End Page': 'dc.identifier.epage',
'Publication Year': 'dc.date.issued',
'Publisher': 'dc.publisher',
'DOI': 'dc.identifier.doi',
'PMID': 'dc.identifier.pmid',
'PMCID': 'dc.identifier.pmc',
'Microsoft Academic ID': 'dc.identifier.mag',
'Lens ID': 'dc.identifier.lens',
'MeSH Terms': 'dc.subject.mesh',
'Fields of Study': 'dc.subject.lens-fields',
'Keywords': 'dc.subject',
'Chemicals': 'dc.subject.chemicals',
'Funding': 'dc.description.sponsorship'
})

## drop all unused columns
df_lens.drop(['Date Published','Source Country','Source URLs','External URL','Cites Patent Count','References','Scholarly Citation Count'], 1, inplace=True)

## convert df to str
df_lens = df_lens.astype(str)

##  remove trailing ".0" after PMID
#df_lens['dc.identifier.pmid'] = df_lens['dc.identifier.pmid'].str.replace('.0', '')

## in abstract field replace html tags with ''
df_lens['dc.description.abstract'].replace({'<[^<]+?>': ''}, inplace=True, regex=True)

## in author field replace ; with ||
df_lens['dc.contributor.author'].replace({'\;': '||'}, inplace=True, regex=True)

## in ISSN replace ; with ||  ### To do: put an hyphen between the groups of four numbers
df_lens['dc.identifier.issn'].replace({'\;': '||'}, inplace=True, regex=True)

# in subject fields replace ; with ||
df_lens['dc.subject'].replace({'\;': '||'}, inplace=True, regex=True)
df_lens['dc.subject.lens-fields'].replace({'\;': '||'}, inplace=True, regex=True)
df_lens['dc.subject.mesh'].replace({'\;': '||'}, inplace=True, regex=True)
df_lens['dc.subject.chemicals'].replace({'\;': '||'}, inplace=True, regex=True)

# unify publication types dc.type
df_lens['dc.type'].replace({'journal article': 'Journal Article'}, inplace=True, regex=True)
df_lens['dc.type'].replace({'conference proceedings': 'Conference Paper'}, inplace=True, regex=True)
df_lens['dc.type'].replace({'conference proceedings article': 'Conference Paper'}, inplace=True, regex=True)
df_lens['dc.type'].replace({'clinical trial': 'Journal Article'}, inplace=True, regex=True)
df_lens['dc.type'].replace({'clinical study': 'Journal Article'}, inplace=True, regex=True)
df_lens['dc.type'].replace({'preprint': 'Preprint'}, inplace=True, regex=True)
df_lens['dc.type'].replace({'book chapter': 'Book Chapter'}, inplace=True, regex=True)
df_lens['dc.type'].replace({'book': 'Book'}, inplace=True, regex=True)
df_lens['dc.type'].replace({'dataset': 'Dataset'}, inplace=True, regex=True)
df_lens['dc.type'].replace({'unknown': 'Unknown'}, inplace=True, regex=True)
df_lens['dc.type'].replace({'letter': 'Letter'}, inplace=True, regex=True)
df_lens['dc.type'].replace({'editorial': 'Editorial'}, inplace=True, regex=True)
df_lens['dc.type'].replace({'report': 'Report'}, inplace=True, regex=True)
df_lens['dc.type'].replace({'other': 'Other'}, inplace=True, regex=True)
df_lens['dc.type'].replace({'news': 'News'}, inplace=True, regex=True)
df_lens['dc.type'].replace({'review': 'Review'}, inplace=True, regex=True)
df_lens['dc.type'].replace({'dissertation': 'Dissertation'}, inplace=True, regex=True)
df_lens['dc.type'].replace({'component': 'Component'}, inplace=True, regex=True)
df_lens['dc.type'].replace({'review': 'Review'}, inplace=True, regex=True)
df_lens['dc.type'].replace({'reference entry': 'Reference Entry'}, inplace=True, regex=True)

# in sponsorship/funder replace ; with ||
df_lens['dc.description.sponsorship'].replace({'\;': '||'}, inplace=True, regex=True)

## all DOIs  in lower case to be on the safe side
df_lens['dc.identifier.doi'] = df_lens['dc.identifier.doi'].str.lower()

df_lens_no_source = df_lens[df_lens['dc.relation.ispartof'] == '']  ## subsetting publications *without* "Source Title" = dc.relation.ispartof
df_lens_no_source_doi = df_lens_no_source[df_lens_no_source['dc.identifier.doi'] != '']  ## subsetting publications *without* "Source Title" but with a DOI
df_lens_preprint = df_lens[df_lens['dc.type'] == 'Preprint']  ## subsetting publications with dc.type = Preprint
df_lens_source = df_lens[df_lens['dc.relation.ispartof'] != '']  ## subsetting publications *with* "Source Title" = dc.relation.ispartof


print(df_lens_no_source_doi)

df_lens.to_csv(r'kyambogo_lens_out.csv', index=False)
df_lens_source.to_csv(r'kyambogo_lens_source_out.csv', index=False)
df_lens_no_source.to_csv(r'kyambogo_lens_no_source_out.csv', index=False)
df_lens_preprint.to_csv(r'kyambogo_lens_preprint_out.csv', index=False)
df_lens_no_source_doi.to_csv(r'kyambogo_lens_no_source_doi_out.csv', index=False)

## Convert a standard The Lens csv to DSpace batch import format
## Anders Wändahl - anders@golonka.se

import pandas as pd
import numpy as np
from datetime import datetime
import re

#df_lens = pd.read_csv("mak_lens_export.csv", delimiter=',', index_col=False) ## import with NaN
#df_lens = pd.read_csv("smak_lens_export.txt", delimiter=',', quotechar='"', index_col=False, na_filter=False) ## import with nothing instead of NaN
df_lens = pd.read_csv("lens-export.csv", delimiter=',', quotechar='"', index_col=False, na_filter=False) ## import with nothing instead of NaN
df_lens.insert(0, 'db_source', 'lens') ## create a new column to the left and fill it with information about the database source "lens" = The Lens
df_lens.insert(0, 'collection', '1/47358') ## create a new column to the left and fill it with the appropriate collection id, for Makerere University in this case
df_lens.insert(0, 'id', '+') ## create a new column to the left and fill it with "+" = import of new records

df_lens['Keywords'].replace({'\\n': ''}, inplace=True, regex=True)
df_lens['Fields of Study'].replace({'\\n': ''}, inplace=True, regex=True)
df_lens['MeSH Terms'].replace({'\\n': ''}, inplace=True, regex=True)
df_lens['Chemicals'].replace({'\\n': ''}, inplace=True, regex=True)
df_lens['Funding'].replace({'\\n': ''}, inplace=True, regex=True)
#df_lens['Funding'].replace({'\\t': ' '}, inplace=True, regex=True)  ## match tab unnecessary! '\\s{2,}' will cover \t too
df_lens['Funding'].replace({'\\s{2,}': ' '}, inplace=True, regex=True) ## match two or more white spaces
df_lens['Source Title'].replace({'\\r\\n': ''}, inplace=True, regex=True) ## match new line
df_lens['Source Title'].replace({'\\s{2,}': ' '}, inplace=True, regex=True)
df_lens['Source Title'].replace({'\\r': ' '}, inplace=True, regex=True) ## match two or more white spaces
df_lens['Source Title'].replace({'\\n': ' '}, inplace=True, regex=True) ## match two or more white spaces
df_lens['Abstract'].replace({'\\r': ''}, inplace=True, regex=True)  ## match carriage return


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

##  remove trailing ".0" after PMID  (WoS)
#df_lens['dc.identifier.pmid'] = df_lens['dc.identifier.pmid'].str.replace('.0', '')

## in abstract field replace html tags with ''
df_lens['dc.description.abstract'].replace({'<[^<]+?>': ''}, inplace=True, regex=True)

## in author field replace ; with ||
df_lens['dc.contributor.author'].replace({'\;': '||'}, inplace=True, regex=True)

## in ISSN replace ; with ||  ### To do: put an hyphen between the groups of four numbers
#df_lens['dc.identifier.issn'].replace('(\d{4})(.{4})', '--------', inplace=True, regex=True)
#df_lens['dc.identifier.issn'] = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", df_lens['dc.identifier.issn'])
#df_lens['dc.identifier.issn'].replace(('(\d{4})(.{4})','$1-$2'), inplace=True, regex=True)
# Where (.{4}) - First capturing group and dot representing anything and exactly 4 times. Where (.{4}) - Second capturing group and dot representing anything and exactly 4 times
# $1- : Represent the first capturing group and add hyphen after that. $2 : Represent the second capturing group and add hyphen after that
df_lens['dc.identifier.issn'].replace({'\;': '||'}, inplace=True, regex=True)

## Capital letters in the beginning of keywords
df_lens['dc.subject'] = df_lens['dc.subject'].str.title()

# in subject fields replace separator ; with ||
df_lens['dc.subject'].replace({'\;': '||'}, inplace=True, regex=True)
df_lens['dc.subject'].replace({'\r\n': ''}, inplace=True, regex=True)
df_lens['dc.subject.lens-fields'].replace({'\;': '||'}, inplace=True, regex=True)
df_lens['dc.subject.lens-fields'].replace({'\r\n': ''}, inplace=True, regex=True) ## I have found a few /r/n that corrupt things
df_lens['dc.subject.mesh'].replace({'\;': '||'}, inplace=True, regex=True)
df_lens['dc.subject.mesh'].replace({'\r\n': ''}, inplace=True, regex=True)
df_lens['dc.subject.chemicals'].replace({'\;': '||'}, inplace=True, regex=True)
df_lens['dc.subject.chemicals'].replace({'\r\n': ''}, inplace=True, regex=True)

# unify publication types dc.type
df_lens['dc.type'].replace({'journal article': 'Journal Article'}, inplace=True, regex=True)
df_lens['dc.type'].replace({'conference proceedings article': 'Conference Paper'}, inplace=True, regex=True)
df_lens['dc.type'].replace({'conference proceedings': 'Conference Paper'}, inplace=True, regex=True)
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

## all DOIs in lower case to be on the safe side
df_lens['dc.identifier.doi'] = df_lens['dc.identifier.doi'].str.lower()

## Subsetting different subfiles
df_lens_no_source = df_lens[df_lens['dc.relation.ispartof'] == '']  ## subsetting publications *without* "Source Title" = dc.relation.ispartof
df_lens_no_source_doi = df_lens_no_source[df_lens_no_source['dc.identifier.doi'] != '']  ## subsetting publications *without* "Source Title" but with a DOI
df_lens_preprint = df_lens[df_lens['dc.type'] == 'Preprint']  ## subsetting publications with dc.type = Preprint
df_lens_source = df_lens[df_lens['dc.relation.ispartof'] != '']  ## subsetting publications *with* "Source Title" = dc.relation.ispartof

## Making CSVs
df_lens.to_csv(r'mak_lens_out.csv', index=False)
df_lens_source.to_csv(r'mak_lens_source_out.csv', index=False)
df_lens_no_source.to_csv(r'mak_lens_no_source_out.csv', index=False)
df_lens_preprint.to_csv(r'mak_lens_preprint_out.csv', index=False)
df_lens_no_source_doi.to_csv(r'mak_lens_no_source_doi_out.csv', index=False)


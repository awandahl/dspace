## Convert a standard WoS tab separated csv to DSpace batch import format XX
## Anders Wändahl - anders@golonka.se

import pandas as pd
import numpy as np
df_wos = pd.read_csv("savedrecs.txt", delimiter='\t', index_col=False, na_filter=False) ## import with nothing instead of NaN
df_wos.insert(0, 'collection', '1/48307') ## create a new column to the left and fill it with the appropriate collection id
df_wos.insert(0, 'id', '+') ## create a new column to the left and fill it with "+" = import of new records

## rename columns from WoS tags to dc-metadata 
df_wos = df_wos.rename(columns={'AR': 'dc.identifier.articleno', 'AB': 'dc.description.abstract', 'AF': 'dc.contributor.author', 'BE': 'dc.contributor.editor', 'BN': 'dc.identifier.isbn', 'BP': 'dc.identifier.spage', 'C1': 'dc.description.affiliation', 'EM': 'dc.description.email', 'CA': 'dc.contributor.group', 'CL': 'dc.description.conf-location', 'CT': 'dc.description.conf', 'CY': 'dc.description.conf-date', 'DE': 'dc.subject', 'DI': 'dc.identifier.doi', 'DT': 'dc.type', 'EI': 'dc.identifier.eissn', 'EP': 'dc.identifier.epage', 'FU': 'dc.description.sponsorship', 'ID': 'dc.subject.kwp', 'IS': 'dc.identifier.issue', 'LA': 'dc.language', 'OA': 'dc.description.oa', 'OI': 'dc.description.orcid', 'PA': 'dc.publisher.address', 'PG': 'dc.description.pages', 'PI': 'dc.publisher.city', 'PM': 'dc.identifier.pmid', 'PU': 'dc.publisher', 'PY': 'dc.date.issued', 'RP': 'dc.description.corr', 'SC': 'dc.subject.sc', 'SN': 'dc.identifier.issn', 'SO': 'dc.relation.ispartof', 'TI': 'dc.title', 'UT': 'dc.identifier.isi', 'VL': 'dc.identifier.volume', 'WC': 'dc.subject.wc'})

## drop all unused columns
df_wos.drop(['FX','SE','BS','BF','BA','AU','PT','GP','SP','HO','RI','CR','NR','TC','Z9','U1','U2','J9','JI','PD','PN','SU','SI','MA','D2','EA','GA','HC','HP','DA'], 1, inplace=True)

## convert df to str
df_wos = df_wos.astype(str)

## remove "WOS:" from ISI-id
df_wos['dc.identifier.isi'].replace({'WOS:': ''}, inplace=True, regex=True)

##  remove trailing ".0" after PMID
#df_wos['dc.identifier.pmid'] = df_wos['dc.identifier.pmid'].str.replace('.0', '')

## replace ; with ||
df_wos['dc.contributor.author'].replace({'\;': '||'}, inplace=True, regex=True)
df_wos['dc.contributor.editor'].replace({'\;': '||'}, inplace=True, regex=True)

df_wos['dc.subject'] = df_wos['dc.subject'].str.title()
df_wos['dc.subject'].replace({'\;': '||'}, inplace=True, regex=True)
df_wos['dc.subject.kwp'].replace({'\;': '||'}, inplace=True, regex=True)
df_wos['dc.description.email'].replace({'\;': '||'}, inplace=True, regex=True)
df_wos['dc.description.orcid'].replace({'\;': '||'}, inplace=True, regex=True)
df_wos['dc.description.sponsorship'].replace({'\;': '||'}, inplace=True, regex=True)
df_wos['dc.subject.wc'].replace({'\;': '||'}, inplace=True, regex=True)
df_wos['dc.subject.sc'].replace({'\;': '||'}, inplace=True, regex=True)

## replace , with ||
df_wos['dc.description.oa'].replace({'\,': '||'}, inplace=True, regex=True)

## remove authors and remain with the affiliations separated by ||
df_wos['dc.description.affiliation'].replace({'\[[^\]]*\]': ''}, inplace=True, regex=True)
df_wos['dc.description.affiliation'].replace({'\;': '||'}, inplace=True, regex=True)

## lowercase except for first letter in every word in journal name
df_wos['dc.relation.ispartof'] = df_wos['dc.relation.ispartof'].str.title()
df_wos['dc.relation.ispartof'].replace({' The ': ' the ', 'Mmwr': 'MMWR', ' In ': ' in ', ' Of ': ' of ', ' For': ' for ', ' And ': ' and ', ' Und ': 'und', ' Des ': ' des ', 'Aids': 'AIDS', 'Hiv': 'HIV', ' Fur ': ' für ', 'Plos One': 'PLOS ONE', 'Plos ': 'PLOS ', 'PLOS One': 'PLOS ONE', 'Bmc ': 'BMC ', 'Ieee': 'IEEE', 'Faseb': 'FASEB', 'Std': 'STD', 'Bmj': 'BMJ', 'Iatss': 'IATSS', 'Ifip': 'IFIP', 'Jama': 'JAMA', 'Jmir': 'JMIR', 'Bba': 'BBA', 'Mbio': 'mBio', 'Peerj': 'PeerJ', ' Et ': ' et ', ' Npj ': 'npj'}, inplace=True, regex=True)

## lowercase except for first letter in every word in KeyWord Plus
df_wos['dc.subject.kwp'] = df_wos['dc.subject.kwp'].str.title()

## all DOIs  in lower case to be on the safe side
df_wos['dc.identifier.doi'] = df_wos['dc.identifier.doi'].str.lower()

################## Scopus goes here ##########################

df_scopus = pd.read_csv("scopus.csv", delimiter=',', index_col=False, na_filter=False) ## import with nothing instead of NaN
df_scopus = df_scopus.astype(str)
df_scopus['Funding Text 1'].replace('\n\n', '||', inplace=True, regex=True)
df_scopus['Funding Text 2'].replace('\n\n', '||', inplace=True, regex=True)
df_scopus['Funding Text 3'].replace('\n\n', '||', inplace=True, regex=True)
df_scopus['Funding Text 4'].replace('\n\n', '||', inplace=True, regex=True)
df_scopus['Funding Text 5'].replace('\n\n', '||', inplace=True, regex=True)
df_scopus['Funding Details'].replace('\n\n', '||', inplace=True, regex=True)

## rename columns from Scopus tags to DSpace dc-metadata
df_scopus = df_scopus.rename(columns={'Art. No.': 'dc.identifier.articleno', 'Abstract': 'dc.description.abstract', 'Authors': 'dc.contributor.author', 'Editors': 'dc.contributor.editor', 'ISBN': 'dc.identifier.isbn', 'Page start': 'dc.identifier.spage', 'Affiliations': 'dc.description.affiliation', 'Conference location': 'dc.description.conf-location', 'Conference name': 'dc.description.conf', 'Conference date': 'dc.description.conf-date', 'Author Keywords': 'dc.subject', 'DOI': 'dc.identifier.doi', 'Document Type': 'dc.type', 'Page end': 'dc.identifier.epage', 'Funding Text 1': 'dc.description.sponsorship', 'Index Keywords': 'dc.subject.scopus', 'Issue': 'dc.identifier.issue', 'Language of Original Document': 'dc.language', 'Open Access': 'dc.description.oa', 'Page count': 'dc.description.pages', 'PubMed ID': 'dc.identifier.pmid', 'Publisher': 'dc.publisher', 'Year': 'dc.date.issued', 'Correspondence Address': 'dc.description.corr', 'ISSN': 'dc.identifier.issn', 'Source title': 'dc.relation.ispartof', 'Title': 'dc.title', 'Volume': 'dc.identifier.volume', 'EID': 'dc.identifier.eid', 'Conference code': 'dc.description.conf-code'})

## drop all unused columns
df_scopus.drop(['Author(s) ID','Cited by','Link','Authors with affiliations','Molecular Sequence Numbers','Chemicals/CAS','Tradenames','Manufacturers','Funding Details','Sponsors','Funding Text 2','Funding Text 3','Funding Text 4','Funding Text 5','References','CODEN','Abbreviated Source Title','Publication Stage','Source'], 1, inplace=True)

##  remove trailing ".0" after PMID
#df_scopus['dc.identifier.pmid'] = df_wos['dc.identifier.pmid'].str.replace('.0', '')

## replace ; with ||
df_scopus['dc.contributor.author'].replace({',': '||'}, inplace=True, regex=True)
df_scopus['dc.contributor.editor'].replace({',': '||'}, inplace=True, regex=True)

df_scopus['dc.subject'] = df_scopus['dc.subject'].str.title()
df_scopus['dc.subject'].replace({'\;': '||'}, inplace=True, regex=True)
df_scopus['dc.subject.scopus'] = df_scopus['dc.subject.scopus'].str.title()
df_scopus['dc.subject.scopus'].replace({'\;': '||'}, inplace=True, regex=True)
df_scopus['dc.description.sponsorship'].replace({'\;': '||'}, inplace=True, regex=True)

## replace , with ||
df_scopus['dc.description.oa'].replace({'\,': '||'}, inplace=True, regex=True)

## remove authors and remain with the affiliations separated by ||
#df_scopus['dc.description.affiliation'].replace({'\[[^\]]*\]': ''}, inplace=True, regex=True)
df_scopus['dc.description.affiliation'].replace({'\;': '||'}, inplace=True, regex=True)

## all DOIs  in lower case to be on the safe side
df_scopus['dc.identifier.doi'] = df_scopus['dc.identifier.doi'].str.lower()

df_scopus['dc.identifier.doi'].replace('', np.nan)
df_scopus.dropna(axis=0, how='any', subset=['dc.identifier.doi'], inplace=True)

################# End of Scopus ##############################

#cols_to_use = df_wos.columns.difference(df_scopus.columns)
#print (cols_to_use)


#df_merge = pd.merge(df_wos, df_scopus, on='dc.identifier.doi', how='inner', suffixes=('', '_scopus'))

print (df_scopus['dc.identifier.doi'])
print (df_wos['dc.identifier.doi'])

#print(df_scopus)
#print (df_wos['dc.identifier.pmid'])
#print (df_merge)

#df_merge = df_merge['dc.identifier.pmid']

#df_scopus.to_csv(r'scopus_out.csv', index=False)
#df_wos.to_csv(r'wos_out.csv', index=False)
#df_merge.to_csv(r'merge_out.csv', index=False)



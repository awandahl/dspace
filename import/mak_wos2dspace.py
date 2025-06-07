## Convert a standard WoS tab separated csv to DSpace batch import format
## Anders Wändahl - anders@golonka.se

import pandas as pd
df = pd.read_csv("savedrecs.txt", delimiter='\t', index_col=False, na_filter=False) ## import with nothing instead of NaN
df.insert(0, 'collection', '1/47358') ## create a new column to the left and fill it with the appropriate collection id
df.insert(0, 'id', '+') ## create a new column to the left and fill it with "+" = import of new records

## rename columns from WoS tags to dc-metadata 
df = df.rename(columns={'AR': 'dc.identifier.articleno', 'AB': 'dc.description.abstract', 'AF': 'dc.contributor.author', 'BE': 'dc.contributor.editor', 'BN': 'dc.identifier.isbn', 'BP': 'dc.identifier.spage', 'C1': 'dc.description.affiliation', 'EM': 'dc.description.email', 'CA': 'dc.contributor.group', 'CL': 'dc.description.conf-location', 'CT': 'dc.description.conf', 'CY': 'dc.description.conf-date', 'DE': 'dc.subject', 'DI': 'dc.identifier.doi', 'DT': 'dc.type', 'EI': 'dc.identifier.eissn', 'EP': 'dc.identifier.epage', 'FU': 'dc.description.sponsorship', 'ID': 'dc.subject.kwp', 'IS': 'dc.identifier.issue', 'LA': 'dc.language', 'OA': 'dc.description.oa', 'OI': 'dc.description.orcid', 'PA': 'dc.publisher.address', 'PG': 'dc.description.pages', 'PI': 'dc.publisher.city', 'PM': 'dc.identifier.pmid', 'PU': 'dc.publisher', 'PY': 'dc.date.issued', 'RP': 'dc.description.corr', 'SC': 'dc.subject.sc', 'SN': 'dc.identifier.issn', 'SO': 'dc.relation.ispartof', 'TI': 'dc.title', 'UT': 'dc.identifier.isi', 'VL': 'dc.identifier.volume', 'WC': 'dc.subject.wc'})

## drop all unused columns
df.drop(['FX','SE','BS','BF','BA','AU','PT','GP','SP','HO','RI','CR','NR','TC','Z9','U1','U2','J9','JI','PD','PN','SU','SI','MA','D2','EA','GA','HC','HP','DA'], 1, inplace=True)

## convert df to str
df = df.astype(str)

## remove "WOS:" from ISI-id
df['dc.identifier.isi'].replace({'WOS:': ''}, inplace=True, regex=True)

##  remove trailing ".0" after PMID
df['dc.identifier.pmid'] = df['dc.identifier.pmid'].str.replace('.0', '')

## replace ; with ||
df['dc.contributor.author'].replace({'\;': '||'}, inplace=True, regex=True)
df['dc.contributor.editor'].replace({'\;': '||'}, inplace=True, regex=True)

df['dc.subject'] = df['dc.subject'].str.title()
df['dc.subject'].replace({'\;': '||'}, inplace=True, regex=True)
df['dc.subject.kwp'].replace({'\;': '||'}, inplace=True, regex=True)
df['dc.description.email'].replace({'\;': '||'}, inplace=True, regex=True)
df['dc.description.orcid'].replace({'\;': '||'}, inplace=True, regex=True)
df['dc.description.sponsorship'].replace({'\;': '||'}, inplace=True, regex=True)
df['dc.subject.wc'].replace({'\;': '||'}, inplace=True, regex=True)
df['dc.subject.sc'].replace({'\;': '||'}, inplace=True, regex=True)

## replace , with ||
df['dc.description.oa'].replace({'\,': '||'}, inplace=True, regex=True)

## remove authors and remain with the affiliations separated by ||
df['dc.description.affiliation'].replace({'\[[^\]]*\]': ''}, inplace=True, regex=True)
df['dc.description.affiliation'].replace({'\;': '||'}, inplace=True, regex=True)

## lowercase except for first letter in every word in journal name
df['dc.relation.ispartof'] = df['dc.relation.ispartof'].str.title()
df['dc.relation.ispartof'].replace({' The ': ' the ', 'Mmwr': 'MMWR', ' In ': ' in ', ' Of ': ' of ', ' For': ' for ', ' And ': ' and ', ' Und ': 'und', ' Des ': ' des ', 'Aids': 'AIDS', 'Hiv': 'HIV', ' Fur ': ' für ', 'Plos One': 'PLOS ONE', 'Plos ': 'PLOS ', 'PLOS One': 'PLOS ONE', 'Bmc ': 'BMC ', 'Ieee': 'IEEE', 'Faseb': 'FASEB', 'Std': 'STD', 'Bmj': 'BMJ', 'Iatss': 'IATSS', 'Ifip': 'IFIP', 'Jama': 'JAMA', 'Jmir': 'JMIR', 'Bba': 'BBA', 'Mbio': 'mBio', 'Peerj': 'PeerJ', ' Et ': ' et ', ' Npj ': 'npj'}, inplace=True, regex=True)

## lowercase except for first letter in every word in KeyWord Plus
df['dc.subject.kwp'] = df['dc.subject.kwp'].str.title()

print (df)
df.to_csv(r'out.csv', index=False)

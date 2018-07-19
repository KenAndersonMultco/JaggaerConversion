import os
import sys
import csv
import GetConfig as g
import contract_help as ch

f = open(g.parmdict['HeaderDataFilePath'],'r')

iodir = g.parmdict['IOFileDirectory']
appdir = g.parmdict['AppDataDirectory']
logdir = g.parmdict['LogFileDirectory']

outputfilename = os.path.join(iodir,'ContractPartyImport.csv')
fout = open(outputfilename,'wb')
mywriter = csv.writer(fout, delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)

lineout = ['PARTY','OverrideDupError','ERPNumber','SciQuestID','ContractPartyName','DoingBusinessAs','OtherNames','CountryofOrigin','Active',
           'ContractPartyType','Primary','LegalStructure','TaxIDType','TaxIdentificationNumber','VATRegistrationNumber','WebsiteURL']
mywriter.writerow(lineout)

colnumlookup = {}
r = open(os.path.join(appdir,'rules.csv'),'r')
for line in csv.reader(r):
    if line[2] <> '':
            colnumlookup[line[0]] = int(line[2])
r.close()

suppliernumberindex = colnumlookup['SecondPartyId']
suppliernameindex = suppliernumberindex + 1

parties = {}

for line in csv.reader(f):
    if line[0] == 'Contract_Name':
            continue
    SupplierID = ch.getSupplierID(line[suppliernumberindex])
    if SupplierID == 'VendorNumberNotFound':
        supnum = line[suppliernumberindex]
        if supnum not in parties.keys():
            parties[supnum] = line[suppliernameindex]

for k,v in parties.items():   
    lineout = []
    lineout.append('PARTY')
    lineout.append('')
    lineout.append(k)
    lineout.append('')
    lineout.append(v)
    lineout.append('')
    lineout.append('')
    lineout.append('')
    lineout.append('FALSE')
    lineout.append('Supplier')
    lineout.append('FALSE')
    lineout.append('')
    lineout.append('')
    lineout.append('')
    lineout.append('')
    lineout.append('')
    mywriter.writerow(lineout)
    
f.close()
fout.close()

import os
import csv
import xml.etree.ElementTree as ET
parmdict = {}
tree = ET.parse('h:/JaggaerDC/config.xml')
root = tree.getroot()
for child in root:
    parmdict[child.tag] = child.text
    

#contractdir = 'R:\\Prod\\BUS2000113'
#contractdir = 'R:\\BUS2000113'
contractdir = parmdict['ContractFileDirectory']
contractfolders = sorted(os.listdir(contractdir))

#rfxdir = 'R:\\BUS2200'
rfxdir = parmdict['RFXFileDirectory']
rfxfolders = sorted(os.listdir(rfxdir))


contractlist = []
rfxdict = {}
rfxnamedict = {}
contract_loaded_count = 0
contract_not_loaded_count = 0
contracts_with_documents_count = 0
contracts_on_input_file_count = 0
contract_file_count = 0
rfx_with_documents_count = 0
rfx_loaded_count = 0
rfx_not_loaded_count = 0
rfx_file_count = 0

#define lists to hold logs for sorting
log1list = []
log2list = []
log3list = []
log4list = []
log5list = []

log1path = os.path.join(parmdict['LogFileDirectory'],'ContractsNotLoaded.csv')
log2path = os.path.join(parmdict['IOFileDirectory'],'ContractFilesLoaded.csv')
log3path = os.path.join(parmdict['LogFileDirectory'],'RFXsNotLoaded.csv')
log4path = os.path.join(parmdict['IOFileDirectory'],'RFxFilesLoaded.csv')
log5path = os.path.join(parmdict['LogFileDirectory'],'ListOfRFxAndAssociatedContracts.csv')
#open log files
log1 = open(log1path,'wb')
log2 = open(log2path,'wb')
log3 = open(log3path,'wb')
log4 = open(log4path,'wb')
log5 = open(log5path,'wb')
log1writer = csv.writer(log1,delimiter = ',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
log2writer = csv.writer(log2,delimiter = ',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
log3writer = csv.writer(log3,delimiter = ',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
log4writer = csv.writer(log4,delimiter = ',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
log5writer = csv.writer(log5,delimiter = ',',quotechar='"',quoting=csv.QUOTE_MINIMAL)


#write log file headers

log1writer.writerow(['ContractNumber','ContractName'])
log2writer.writerow(['ContractFolder','ContractFileName'])
log3writer.writerow(['RFxNumber','RFxName'])
log4writer.writerow(['RFxFolder','RFxFileName'])
log5writer.writerow(['RFxNumber','RFxName','AssociatedContractNumber','AssociatedContractName'])


#read the FM folders and build an RFX Number to RFx Name dictionary

for z in rfxfolders:
    rfxnum = z[0:10]
    rfxname = z[11:]
    rfxnamedict[rfxnum] = rfxname

#build a list of contract numbers and associated RFx numbers
#with open('h:/JaggaerDC/ContractData.csv','r') as contractdata:
with open(parmdict['HeaderDataFilePath'],'r') as contractdata:
    for line in csv.reader(contractdata):
        contracts_on_input_file_count += 1
        contractnum = line[11]
        contractname = line[0]
        contractlist.append(contractnum)
        #dict with rfx as key, list of associated contract as value becase rfx can be
        #associated to multiple contracts
        if line[12] <> '':
            for r in line[12].split(';'):
                log5line = []
                log5line.append(r)
                log5line.append(rfxnamedict.get(r,'Files not found for this RFX number'))
                log5line.append(contractnum)
                log5line.append(contractname)
                #log5line = [r,contractnum]
                #need to include rfxname and contract name; use get function for rfx
                
                #log5writer.writerow(log5line)
                log5list.append(log5line)
                
                if r in rfxdict.keys():
                    wlist = rfxdict[r]
                    wlist.append(contractnum)
                    rfxdict[r] = wlist
                else:
                    clist = []
                    clist.append(contractnum)
                    rfxdict[r] = clist
    

#do validation stuff
print 'validating'
for f in contractfolders:
    contracts_with_documents_count += 1
    contract_nbr = f[0:10]
    contract_name = f[11:]
    if contract_nbr in contractlist:
        contract_loaded_count += 1
        #write to log 2
        for fname in os.listdir(os.path.join(contractdir,f)):
            lineout = []
            contract_file_count += 1
            #filepath = os.path.join(contractdir,f,fname)
            lineout.append(f)
            lineout.append(fname)
            #log2writer.writerow(lineout)
            log2list.append(lineout)
    else:
        #write to log 1
        contract_not_loaded_count += 1
        lineout = []
        lineout.append(contract_nbr)
        lineout.append(contract_name)
        #log1writer.writerow(lineout)
        log1list.append(lineout)
for rx in rfxfolders:
    rfx_with_documents_count += 1
    rfx_nbr = rx[0:10]
    rfx_name = rx[11:]
    if rfx_nbr in rfxdict.keys():
        rfx_loaded_count += 1
        #write to log 4
        for fname in os.listdir(os.path.join(rfxdir,rx)):
            lineout = []
            rfx_file_count += 1
            lineout.append(rx)
            lineout.append(fname)
            #log4writer.writerow(lineout)
            log4list.append(lineout)
    else:
        #write to log 3
        rfx_not_loaded_count += 1
        lineout = []
        lineout.append(rfx_nbr)
        lineout.append(rfx_name)
        #log3writer.writerow(lineout)
        log3list.append(lineout)
 
#sort log lists and write to files

log1list.sort(key=lambda line: line[0])
log2list.sort(key=lambda line: line[0])
log3list.sort(key=lambda line: line[0][0:10] + line[1][0:5])
log4list.sort(key=lambda line: line[0][0:10] + line[1][0:5])
log5list.sort(key=lambda line: line[0] + line[2])

for l in log1list:
    log1writer.writerow(l)
for l in log2list:
    log2writer.writerow(l)
for l in log3list:
    log3writer.writerow(l)
for l in log4list:
    log4writer.writerow(l)
for l in log5list:
    log5writer.writerow(l)
    
#contractdata.close()
log1.close()
log2.close()
log3.close()
log4.close()
log5.close()

print 'Count of contracts on the header conversion input file is ' + str(contracts_on_input_file_count)
print 'Total count of contracts with exported documents is ' + str(contracts_with_documents_count)
print 'Count of contracts with documents found on header conversion input file is ' + str(contract_loaded_count)
print 'Count of contracts with documents not found on header conversion input file is ' + str(contract_not_loaded_count)
print 'Count of contract files (to be) loaded is ' + str(contract_file_count)
print 'Count of RFXs with documents is ' + str(rfx_with_documents_count)
print 'Count of RFXs with not documents not associated to a contract on header input file is ' + str(rfx_not_loaded_count)
print 'Count of RFx files (to be) loaded is ' + str(rfx_file_count)
print 'Count of RFXs not loaded is ' + str(rfx_not_loaded_count)





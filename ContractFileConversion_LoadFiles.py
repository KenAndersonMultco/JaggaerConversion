import os
import csv
import pysftp

#prompt user to select top level folder for documents
#updated to simplify since all top level contract folders will contain all files


#ftplib does not support sftp
#fortunately, there is pysftp which works

#The following section connects to FTP site and
#getting list of files currently there

mode = raw_input('(v)alidate or (l)oad files to FTP site\n')
#contractdir = 'R:\\Prod\\BUS2000113'
contractdir = 'R:\\BUS2000113'
contractfolders = sorted(os.listdir(contractdir))
contractdata = open('h:/JaggaerDC/ContractData.csv','r')
contractlist = []
contract_loaded_count = 0
contract_not_loaded_count = 0
contracts_with_documents_count = 0
contracts_on_input_file_count = 0
file_count = 0

#open log files
log1 = open('h:/JaggaerDC/ContractsNotLoaded.csv','wb')
log2 = open('h:/JaggaerDC/ContractFilesLoaded.csv','wb')
log1writer = csv.writer(log1,delimiter = ',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
log2writer = csv.writer(log2,delimiter = ',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
#build a list of contract numbers
for line in csv.reader(contractdata):
    contractlist.append(line[11])
    contracts_on_input_file_count += 1

if mode == 'v':
    #do validation stuff
    print 'validating'
    for f in contractfolders:
        contracts_with_documents_count += 1
        contract_nbr = f[0:10]
        if contract_nbr in contractlist:
            contract_loaded_count += 1
            #write to log 2
            for fname in os.listdir(os.path.join(contractdir,f)):
                lineout = []
                file_count += 1
                #filepath = os.path.join(contractdir,f,fname)
                lineout.append(contract_nbr)
                lineout.append(fname)
                log2writer.writerow(lineout)          
        else:
            #write to log 1
            contract_not_loaded_count += 1
            lineout = []
            lineout.append(contract_nbr)
            log1writer.writerow(lineout)
            
    
elif mode == 'l':
    print "i would load now if the code wasn't commented out"
##    cnopts = pysftp.CnOpts()
##    cnopts.hostkeys = None
##    srv = pysftp.Connection(host='files.sciquest.com',username='multnomah_ken',
##                            password='multco4sc1qu3st', cnopts=cnopts)
##    #dir = 'R:\BUS2000113'
##    #dir = 'R:\\1Test'

##    for f in contractfolders:
##        contract_nbr = f[0:10]
##        if contract_nbr in contractlist:
##            for fname in os.listdir(os.path.join(contractdir,f)):
##                filepath = os.path.join(contractdir,f,fname)
##                srv.put(filepath)
##
##    srv.close()
else:
    print 'invalid input'
contractdata.close()
log1.close()
log2.close()
print 'Count of contracts on the header conversion input file is ' + str(contracts_on_input_file_count)
print 'Total count of contracts with exported documents is ' + str(contracts_with_documents_count)
print 'Count of contracts with documents found on header conversion input file is ' + str(contract_loaded_count)
print 'Count of contracts with documents not found on header conversion input file is ' + str(contract_not_loaded_count)
print 'Count of files (to be) loaded is ' + str(file_count)






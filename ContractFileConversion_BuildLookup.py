import os
import csv


#prompt user to select top level folder for documents or put in a config file



contractdata = open('h:/JaggaerDC/ContractData.csv','r')
fout = open('h:/JaggaerDC/ContractFileData.csv','wb')
mywriter = csv.writer(fout,delimiter = ',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
contract_rfx = {}
rfx_contract = {}

#read contract data file to get contract/rfx cross-reference

for line in csv.reader(contractdata):
    if line[12] <> '':
        rfxnums = line[12].split(';')
        contract_rfx[line[11]] = rfxnums
        for q in rfxnums:
            rfx_contract[q] = line[11]

#Build lookup file with contract name and associated documents


contractdir = 'R:\Prod\BUS2000113'
rfxdir = 'R:\BUS2200'
#dir = 'R:\\1Test'
rfxfolders = sorted(os.listdir(rfxdir))
contractfolders = sorted(os.listdir(contractdir))
contractfilecount = 0
rfxfilecount = 0 

#process directory with rfx docs and build an rfx # to file name dictionary
rfxdict = {}

#only do this if rfx is associated to a contract on the input file
#this is so it will match the number of files uploaded, or at least be close
for rfxf in rfxfolders:
    RFxNumber = rfxf[0:10]
    if RFxNumber in rfx_contract:
        rfxfilenames = []
        for rfxfname in os.listdir(os.path.join(rfxdir,rfxf)):
            rfxfilecount += 1
            rfxfilenames.append(rfxfname)
        rfxdict[RFxNumber] = rfxfilenames
    else:
        print 'RFx Number ' + RFxNumber + ' is not associated with a contract on the conversion input file'
        
for f in contractfolders:
    ContractNumber = f[0:10]
    if ContractNumber in contract_rfx:
        lineout = []
        namelist = []
        maxfilename = ''
        maxfilesize = 0
        for fname in os.listdir(os.path.join(contractdir,f)):
            contractfilecount += 1
            namelist.append(fname)
            filepath = os.path.join(contractdir,f,fname)
            size = os.path.getsize(filepath)
            if size > maxfilesize:
                maxfilename = fname
                maxfilesize = size
            #displayname = fname2[17:]
            #print displayname, size
            #print 'largest file is',maxfilename

        #build lookup file row
        lineout.append(ContractNumber)
        #write main document
        lineout.append(maxfilename[17:]+'!'+maxfilename)
        #get additional contract attachments
        attachments = ''
        for x in namelist:
            if x != maxfilename:
                filestuff = x[17:] + '!' + x
                if attachments == '':
                    attachments = attachments + filestuff
                else:
                    attachments = attachments + '|' +  filestuff
        #add in rfx docs
        contractrelatedrfx = contract_rfx[ContractNumber]
        for crfx in contractrelatedrfx:
            if crfx in rfxdict:
                rfxdoclist = rfxdict[crfx]
                for z in rfxdoclist:
                    rfxstuff = z[6:] + '!' + z
                    if attachments == '':
                        attachments = attachments + rfxstuff
                    else:
                        attachments = attachments + '|' +  rfxstuff
            else:
                print 'rfx ' + crfx + ' associated with contract ' + ContractNumber + ' does not have any files'
        lineout.append(attachments)
        mywriter.writerow(lineout)
    else:
        print 'Contract #' + ContractNumber + ' was not found the contract conversion input file.  It may not be active'

print str(rfxfilecount) + ' rfx files read'
print str(contractfilecount) + ' contract files read.'
fout.close()
contractdata.close()






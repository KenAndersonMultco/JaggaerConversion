import os
import csv
import GetConfig as g

def IsNotAmendment(fname):
    fname1 = fname[0:5]
    fname2 = fname[6:16]
    fname3 = fname[17:19]
    fname4 = fname[20:24]
    fname5 = fname[25:26]
    if fname3 == fname2[0:2] and fname4 == fname2[6:10] and fname[24:25] == '-':
        return False
    else:
        return True

def GetFileExtension(fname):
    #goal is to sort files by pdf, docx and then by filesize.  ie. largest docx if docx exists else largest pdf
    x = fname.find('.')
    if x == -1:
        return 'a-none'
    else:
        ext = fname[x+1:]
        if ext == 'pdf':
            return 'c-pdf'
        elif ext == 'docx':
            return 'd-docx'
        else:
            return 'b-other'

def GetMainFile(folderpath):

    candidates = []
    notfounds = []
    ecfound = False
    corefound = False
    mainfilename = ''
    namelist = []
    for fname in os.listdir(folderpath):   
        namelist.append(fname)
        if fname.find('Executed Contract') > -1:        
            mainfilename = fname
            ecfound = True
        elif (fname.find('Executed') > -1 or fname.find('Contract') > -1 or fname.find('CON') > -1) and not fname.find('Amendment') > -1:
            if IsNotAmendment(fname):
                line = []
                corefound = True 
                line.append(fname)
                try:
                    line.append(round(os.path.getsize(os.path.join(folderpath,fname))/1024.0))
                except WindowsError, e:
                    print 'Windows error ', e.winerror
                    print e.strerror
                    print 'foldername: ',folderpath
                    print 'filename: ', fname
                    return 'filenameerror',[]
                line.append(GetFileExtension(fname))
                candidates.append(line)
        else:
            if IsNotAmendment(fname):
                line = []
                line.append(fname)
                try:
                    line.append(round(os.path.getsize(os.path.join(folderpath,fname))/1024.0))
                except WindowsError, e:
                    print 'Windows error ', e.winerror
                    print e.strerror
                    print 'foldername: ', folderpath
                    print 'filename: ', fname
                    return 'filenameerror',[]    
                line.append(GetFileExtension(fname))
                notfounds.append(line)
    if ecfound:
        return mainfilename, namelist
    elif corefound:
        finalcandidates = []
        for l in candidates:
            if l[0].find('Executed') > -1:
                l.append('c-Executed')
                finalcandidates.append(l)
            elif l[0].find('Contract') > -1:
                l.append('a-Contract')
                finalcandidates.append(l)
            elif l[0].find('CON') > -1:
                l.append('b-CON')
                finalcandidates.append(l)  
        slist = sorted(finalcandidates, key=lambda thing: [thing[3],thing[1]])
        mainfilename = slist[-1][0]
        return mainfilename, namelist
    else:
        slist2 = sorted(notfounds, key=lambda thing: [thing[2],thing[1]])
        mainfilename = slist2[-1][0]
        return mainfilename, namelist

#prompt user to select top level folder for documents or put in a config file

iofiledir = g.parmdict['IOFileDirectory']
logfiledir = g.parmdict['LogFileDirectory']

contractdata = open(g.parmdict['HeaderDataFilePath'],'r')
#fout = open('h:/JaggaerDC/ContractFileData.csv','wb')
fout = open(os.path.join(iofiledir,'ContractFileData.csv'),'wb')
log = open(os.path.join(logfiledir,'ContractFileXrefLog.csv'),'wb')
log2 = open(os.path.join(logfiledir,'AttachmentsNotIncluded.csv'),'wb')
mywriter = csv.writer(fout,delimiter = ',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
logwriter = csv.writer(log,delimiter = ',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
logwriter2 = csv.writer(log2,delimiter = ',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
contract_rfx = {}
rfx_contract = {}
contractheaders = []

#read contract data file to get contract/rfx cross-reference

for line in csv.reader(contractdata):
    contractheaders.append(line[13])
    if line[12] <> '':
        rfxnums = list(set(line[14].split(';')))
        contract_rfx[line[13]] = rfxnums
        for q in rfxnums:
            rfx_contract[q] = line[14]

#Build lookup file with contract name and associated documents


contractdir = g.parmdict['ContractFileDirectory']
rfxdir = g.parmdict['RFXFileDirectory']
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
        logline = []
        line = 'RFx Number ' + RFxNumber + ' is not associated with a contract on the conversion input file'
        logline.append(line)
        logwriter.writerow(logline)

for f in contractfolders:
    ContractNumber = f[0:10]
    if ContractNumber in contractheaders:
        lineout = []
        #namelist = []
        #maxfilename = ''
        #maxfilesize = 0
        #for fname in os.listdir(os.path.join(contractdir,f)):
        #    contractfilecount += 1
        #    namelist.append(fname)
        #    filepath = os.path.join(contractdir,f,fname)
        #    size = os.path.getsize(filepath)
        #    if size > maxfilesize:
        #        maxfilename = fname
        #        maxfilesize = size
            #displayname = fname2[17:]
            #print displayname, size
            #print 'largest file is',maxfilename

        maindoc, namelist = GetMainFile(os.path.join(contractdir,f))
        contractfilecount += len(namelist)
        #build lookup file row
        lineout.append(ContractNumber)
        #write main document
        maintitle = maindoc[17:]
        if len(maintitle) > 100:
            maintitle = maindoc[17:117]
        lineout.append(maintitle+'!'+maindoc)
        #get additional contract attachments
        attachments = ''


        
        for x in namelist:
            notincluded = []
            if x != maindoc:
                attachmenttitle = x[17:]
                if len(attachmenttitle) > 100:
                    attachmenttitle = x[17:117]
                filestuff = attachmenttitle + '!' + x
                if attachments == '':
                    attachments = attachments + filestuff
                else:
                    if len(attachments) + len(filestuff) + 1 < 32768:
                        attachments = attachments + '|' +  filestuff
                    else:
                        print ContractNumber + ' has too many attachments (in contract docs)'
                        notincluded.append(ContractNumber)
                        notincluded.append(x)
                        logwriter2.writerow(notincluded)
                        #need to keep log of documents that won't be uploaded

        #add in rfx docs IF THE CONTRACT HAS ASSOCIATED RFX FILES!
        if ContractNumber in contract_rfx:
            if len(attachments) < 32768:
                contractrelatedrfx = contract_rfx[ContractNumber]
                for crfx in contractrelatedrfx:
                    if crfx in rfxdict:
                        rfxdoclist = rfxdict[crfx]
                        for z in rfxdoclist:
                            notincluded = []
                            rfxdoctitle = z[6:]
                            if len(rfxdoctitle) > 100:
                                rfxdoctitle = z[6:106]
                            rfxstuff = rfxdoctitle + '!' + z
                            if attachments == '':
                                attachments = attachments + rfxstuff
                            else:
                                if len(attachments) + len(filestuff) + 1 < 32768:
                                    attachments = attachments + '|' +  rfxstuff
                                else:
                                    print ContractNumber + 'has too many attachments (in rfx docs)'
                                    notincluded.append(ContractNumber)
                                    notincluded.append(z)
                                    logwriter2.writerow(notincluded)
                                    #need to log
                    else:
                        logline = []
                        line =  'rfx ' + crfx + ' associated with contract ' + ContractNumber + ' does not have any files'
                        logline.append(line)
                        logwriter.writerow(logline)
            else:
                print ContractNumber + 'already has too many attachments.  Not loading rfx docs'
            #need to log docs that won't be loaded
        #there was some reason why I needed to put in 'NA' here but now I don't remember.  It causes an error on the import file
        #so need logic on the contractconversion to blank it out
        if attachments == '':
            attachments = 'NA'
        if len(attachments) > 32767:
            print f + ' has too many attachments to fit in an Excel cell and may not be importable'
            lineout.append(attachments)
        else:
            lineout.append(attachments)
        mywriter.writerow(lineout)
    else:
        logline = []
        line = 'Contract #' + ContractNumber + ' was not found on the contract conversion input file.  It may not be active'
        logline.append(line)
        logwriter.writerow(logline)

print str(rfxfilecount) + ' rfx files read'
print str(contractfilecount) + ' contract files read.'
fout.close()
log.close()
log2.close()
contractdata.close()






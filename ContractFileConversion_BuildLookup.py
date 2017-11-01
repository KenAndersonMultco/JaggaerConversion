import os
import csv


#prompt user to select top level folder for documents


fout = open('h:/JaggaerDC/ContractFileData.csv','wb')
mywriter = csv.writer(fout,delimiter = ',',quotechar='"',quoting=csv.QUOTE_MINIMAL)

#Build lookup file with contract name and associated documents

dir = 'R:\BUS2000113'
contractfolders = sorted(os.listdir(dir))

for f in contractfolders:
    ContractNumber = f[0:10]
    lineout = []
    namelist = []
    maxfilename = ''
    maxfilesize = 0
    for fname in os.listdir(os.path.join(dir,f)):       
        namelist.append(fname)
        filepath = os.path.join(dir,f,fname)
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
    #get additional attachments
    attachments = ''
    for x in namelist:
        if x != maxfilename:
            filestuff = x[17:] + '!' + x
            if attachments == '':
                attachments = attachments + filestuff
            else:
                attachments = attachments + '|' +  filestuff
    lineout.append(attachments)
    mywriter.writerow(lineout)

fout.close()






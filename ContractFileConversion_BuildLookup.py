import os
import csv


#prompt user to select top level folder for documents

#adding a comment to test working with Github

##for fname in os.listdir('\\nas3\CW-IT\Projects\RM_Docs\BUS2000113'):
##    print fname


##dir = 'R:\BUS2000113'
##for fname in os.listdir(dir):
##    fpath = os.path.join(dir,fname)
##    print fname,os.path.isfile(fpath), os.path.isdir(fpath)


fout = open('h:/JaggaerDC/ContractFileData.csv','wb')
mywriter = csv.writer(fout,delimiter = ',',quotechar='"',quoting=csv.QUOTE_MINIMAL)



#Build lookup file with contract name and associated documents

dir = 'R:\BUS2000113'
contractfolders = sorted(os.listdir(dir))

for f in contractfolders:
    cdir = os.path.join(dir,f)
    ContractNumber = f[0:10]
    print 'Contract Number is',ContractNumber
    for root, dirs, files in os.walk(cdir):
        if len(dirs) == 0 and len(files) > 0:  #this is a tuple that has files
            #filenames = ''
            maxfilename = ''
            maxfilesize = 0
            namelist = []
            lineout = []
            for fname in files:
                namelist.append(fname)
                filepath = os.path.join(root,fname)
                size = os.path.getsize(filepath)
                if size > maxfilesize:
                    maxfilename = fname
                    maxfilesize = size
                #displayname = fname2[17:]
                #print displayname, size
            #print 'largest file is',maxfilename

            #build lookup file row
            #
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

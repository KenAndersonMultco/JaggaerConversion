import os
import csv
import math as m

contractfiles = open('h:/JaggaerDC/ContractFilesLoaded.csv','r')
rfxfiles = open('h:/JaggaerDC/RFxFilesLoaded.csv','r')

batchsize = 500.0


cfread = csv.reader(contractfiles)
rfread = csv.reader(rfxfiles)

#subtract 1 from filecounts to account for header row
cfilecount = sum(1 for row in cfread) - 1
rfilecount = sum(1 for row in rfread) - 1

cbatchcount = int(m.ceil(cfilecount / batchsize))
rbatchcount = int(m.ceil(rfilecount / batchsize))
crange = range(1,cbatchcount + 1)
rfxrange = range(1,rbatchcount + 1)
clinecount = 1
currentbatch = 0
rlinecount = 1
rfxcurrentbatch = 0
print 'number of contract files is ' + str(cfilecount)
print 'number of rfx files is ' + str(rfilecount)
print 'contract batches:'
print cbatchcount
print 'rfx batches:'
print rbatchcount

fileobjects = []
writers = []
rfxfileobjects = []
rfxwriters = []
#for line in cfread:
    
for i in crange:
    filename = 'ContractBatch_' + str(i) + '.csv'
    filepath = 'h:/JaggaerDC/Batches/Contract/' + filename
    batchfile = open(filepath,'wb')
    fileobjects.append(batchfile)
    writers.append(csv.writer(batchfile,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL))
for j in rfxrange:
    filename = 'RFxBatch_' + str(j) + '.csv'
    filepath = 'h:/JaggaerDC/Batches/RFx/' + filename
    batchfile = open(filepath,'wb')
    rfxfileobjects.append(batchfile)
    rfxwriters.append(csv.writer(batchfile,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL))

contractfiles.seek(0)
rfxfiles.seek(0)

for line in cfread:
    if clinecount == 1:
        clinecount += 1
        continue
    else:    
        if clinecount % batchsize == 0:
            currentbatch += 1
        writers[currentbatch].writerow(line)
        clinecount += 1
for line in rfread:
    if rlinecount == 1:
        rlinecount += 1
        continue
    else:    
        if rlinecount % batchsize == 0:
            rfxcurrentbatch += 1
        rfxwriters[rfxcurrentbatch].writerow(line)
        rlinecount += 1
for fi in fileobjects:
    fi.close()
for fi in rfxfileobjects:
    fi.close()
contractfiles.close()
rfxfiles.close()

import os, csv
import GetConfig as g

iofiledir = g.parmdict['IOFileDirectory']
headers = open(os.path.join(iofiledir,'ContractDataOut.csv'),'r')
rfxdict = {}
norfx = []
headerdict = {}
contracts_processed = []
idx = 1
#build rfx to contracts xref dictionary
#key is rfx#, value is list of associated contracts
for idx, line in enumerate(csv.reader(headers)):
    if idx == 0:
            colheaders = line
    else:
        headerdict[line[34]] = line
        cnum = line[34]
        rfx = line[35]
        if rfx == '':
            norfx.append(cnum)
        else:
            rfxnums = list(set(rfx.split(';')))
            for x in rfxnums:
                if x in rfxdict:
                    if cnum not in rfxdict[x]:
                        rfxdict[x].append(cnum)
                else:
                    rfxdict[x] = [cnum]
            
#looking good, next sort by length of list, print k, len list, cnums

##for k,v in sorted(rfxdict.items(),key=lambda (k,v): (len(v),k),reverse=True):
###for k,v in rfxdict.items():
##    cnums = ''
##    for cn in v:
##        cnums = cnums + cn + ', '
##    print k,len(v),cnums

maxkey = ''
maxlen = 0
for k,v in rfxdict.items():
    if len(v) > maxlen:
        maxkey = k
        maxlen = len(v)
#maxlen determines the number of batches
fileobjects = []
writers = []
brange = range(1,maxlen + 1)
batchdict = {}
for i in brange:
    filename = 'ImportBatch_' + str(i) + '.csv'
    filepath = os.path.join(iofiledir,'JaggaerImportFiles',filename)
    batchfile = open(filepath,'wb')
    fileobjects.append(batchfile)
    writers.append(csv.writer(batchfile,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL))
    bdindex = i - 1
    batchdict[bdindex] = []
for w in writers:
    w.writerow(colheaders)

current_batch = 0


for k,v in sorted(rfxdict.items(),key=lambda (k,v): (len(v),k),reverse=True):
    print 'rfx is ' + k
    for c in v:
        if c in contracts_processed:
            continue
        else:
            #print k+'|'+c+'|'+ str(current_batch)
            conflictfound = False
            contractrfxlist = list(set(headerdict[c][35].split(';')))
            #print 'current batch is ' + str(current_batch), 'contract is ' + c
            for coisa in contractrfxlist:
                #print 'assoc rfx is ' + coisa
                if coisa in batchdict[current_batch]:
                    #print 'conflict found'
                    conflictfound = True
            while conflictfound is True:
                current_batch = (current_batch + 1) % maxlen
                conflictfound = False
                #print 'new current batch is ' + str(current_batch)
                for coisa in contractrfxlist:
                    if coisa in batchdict[current_batch]:
                        #print 'conflict found for ' + coisa
                        conflictfound = True
            contracts_processed.append(c)
            #print 'writing contract ' + c + ' to batch ' + str(current_batch)
            writers[current_batch].writerow(headerdict[c])
            for coisa in contractrfxlist:
                batchdict[current_batch].append(coisa)
            current_batch = (current_batch + 1) % maxlen
for c in norfx:
    #print 'norfx'+'|'+c+'|'+ str(current_batch)
    writers[current_batch].writerow(headerdict[c])
    current_batch = (current_batch + 1) % maxlen

for fi in fileobjects:
    fi.close()
           
headers.close()

import os
import csv
import pysftp
from datetime import datetime

contractdir = 'R:\\QA\\BUS2000113'
rfxdir = 'R:\\RFx\\BUS2200'
cfiledir = 'S:/JaggaerConversion/IOFiles/Batches/Contract'
rfiledir = 'S:/JaggaerConversion/IOFiles/Batches/RFx'

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
##Sandbox
##srv = pysftp.Connection(host='files.sciquest.com',username='multnomah_ken',
##                        password='multco4sc1qu3st', cnopts=cnopts)
#QA
srv = pysftp.Connection(host='files.sciquest.com',username='multnomahtest_ken',
                        password='tcm4multco', cnopts=cnopts, log='h:/JaggaerDC/pysftp_log.txt')
contractbatches = os.listdir(cfiledir)
rfxbatches = os.listdir(rfiledir)
counter = 0
#fileobjects = []                
for f in contractbatches:
    print f
    print 'started at ' + str(datetime.now())
    filepath = cfiledir + '/' + f
    with open(filepath, 'r') as batchfile:
        for line in csv.reader(batchfile):
            try:
                srv.put(os.path.join(contractdir,line[0],line[1]))
                counter += 1
            except WindowsError, e:
                print 'Windows error ', e.winerror
                print e.strerror
                print 'foldername: ', line[0]
                print 'filename: ', line[1]
            except IOError as e:
                print "I/O error({0}: {1}".format(e.errno, e.strerror)
                print 'foldername: ', line[0]
                print 'filename: ', line[1]
    print 'finished at ' + str(datetime.now())
for f in rfxbatches:                   
    print f
    print 'started at ' + str(datetime.now())
    filepath = rfiledir + '/' + f
    with open(filepath, 'r') as batchfile:
        for line in csv.reader(batchfile):
            try:
                srv.put(os.path.join(rfxdir,line[0],line[1]))
                counter += 1
            except WindowsError, e:
                print 'Windows error #', e.winerror
                print e.strerror
                print 'foldername: ', line[0]
                print 'filename: ', line[1]
            except IOError as e:
                print "I/O error({0}: {1}".format(e.errno, e.strerror)
                print 'foldername: ', line[0]
                print 'filename: ', line[1]
    print 'finished at ' + str(datetime.now())
print counter
    
srv.close()


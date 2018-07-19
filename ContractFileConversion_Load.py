import os
import csv
import pysftp
from datetime import datetime
import GetConfig as g

contractdir = g.parmdict['ContractFileDirectory']
rfxdir = g.parmdict['RFXFileDirectory']
cfiledir = g.parmdict['ContractBatchDirectory']
rfiledir = g.parmdict['RFXBatchDirectory']
ftphost = g.parmdict['FTPHost']
ftpusername = g.parmdict['FTPUsername']
ftppassword = g.parmdict['FTPPassword']
logfile = os.path.join(g.parmdict['LogFileDirectory'],'JaggaerFTPlog.txt')
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
##Sandbox
##srv = pysftp.Connection(host='files.sciquest.com',username='multnomah_ken',
##                        password='multco4sc1qu3st', cnopts=cnopts)
#QA
##srv = pysftp.Connection(host='files.sciquest.com',username='multnomahtest_ken',
##                        password='tcm4multco', cnopts=cnopts, log='h:/JaggaerDC/pysftp_log.txt')
#Prod
srv = pysftp.Connection(host=ftphost,username=ftpusername,
                        password=ftppassword, cnopts=cnopts, log=logfile)
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


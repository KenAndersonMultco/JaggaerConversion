import os
import csv


#prompt user to select top level folder for documents
#updated to simplify since all top level contract folders will contain all files



#The following section connects to FTP site and getting list of files currently there

#ftplib does not support sftp
#fortunately, there is pysftp which works

import pysftp
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
srv = pysftp.Connection(host='files.sciquest.com',username='multnomah_ken',
                        password='multco4sc1qu3st', cnopts=cnopts)
#dir = 'R:\BUS2000113'
#dir = 'R:\\1Test'
dir = 'R:\\Prod\\BUS2000113'
contractfolders = sorted(os.listdir(dir))
for f in contractfolders:
    for fname in os.listdir(os.path.join(dir,f)):
        filepath = os.path.join(dir,f,fname)
        srv.put(filepath)


srv.close()







import os
import csv


#prompt user to select top level folder for documents




#The following section connects to FTP site and getting list of files currently there

#ftplib does not support sftp
#fortunately, there is pysftp which works

import pysftp
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
srv = pysftp.Connection(host='files.sciquest.com',username='multnomah_ken',
                        password='multco4sc1qu3st', cnopts=cnopts)
dir = 'R:\BUS2000113'
contractfolders = sorted(os.listdir(dir))
for f in contractfolders:
    cdir = os.path.join(dir,f)
    for root, dirs, files in os.walk(cdir):
        if len(dirs) == 0 and len(files) > 0:
            for fname in files:
                filepath = os.path.join(root,fname)
                srv.put(filepath)


srv.close()




for fname in os.listdir(dir):
    fpath = os.path.join(dir,fname)
    if os.path.isdir(fpath):
        for fname2 in os.listdir(fpath):
            srv.put(os.path.join(fpath,fname2))
    data = srv.listdir()
    
srv.close()

for i in data:
    print i


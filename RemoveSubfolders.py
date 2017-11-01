import os

#Run this script prior to building filename lookup and uploading files

dir = 'R:\BUS2000113'

contractfolders = sorted(os.listdir(dir))
for f in contractfolders:
    top = os.path.join(dir,f)
    tobedeleted = []
    for root, dirs, files in os.walk(top):
        #print top, root, len(dirs), len(files)
        if root <> top and len(dirs) > 0 and len(files) == 0:
            tobedeleted.append(root)
        if root <> top and len(dirs) == 0 and len(files) > 0:
            for f in files:
                os.rename(os.path.join(root,f),os.path.join(top,f))
            print 'about to delete ',root
            os.rmdir(root)
    for d in tobedeleted:
        print 'about to delete', d
        os.rmdir(d)

                        
        
                

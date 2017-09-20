import csv
import editdistance
import os



if os.getcwd() == 'C:\Python27\Scripts\MyScripts':
    foldername = 'H:\JaggaerDC\AppData'
else:
    foldername = 'AppData'

def formatDate(date):
    parts = date.split('/')
    return parts[2] + '-' + parts[0] + '-' + parts[1] + ' 12:00 AM'
def getFY(date):
    parts = date.split('/')
    if int(parts[0]) > 6:
        return str(int(parts[2])+1)
    else:
        return parts[2]
def getManagerStakeholder(owner,support):
    if owner == '' and support == '':
        manager = 'Heidi Leibbrandt'
        stakeholder = ''
    elif owner == '':
        manager = support
        stakeholder = ''
    elif support == '':
        manager = owner
        stakeholder = ''
    elif owner == support:
        manager = support
        stakeholder = ''
    else:
        manager = support
        stakeholder = owner
    return manager,stakeholder
def getUserID(name):
    nw = name.split()
    name_elements = len(nw)
    #get last name
    ln = nw[name_elements-1].lower()
    #get first name
    fn = ''
    for i in range(0,name_elements-1):
        fn = fn + nw[i].lower()
    if ln in users:
        #try to match first name
        fnamedict = users[ln]
        if fn in fnamedict:
            stakeholder = fnamedict[fn]
        elif len(fnamedict) == 1:
            fn = fnamedict.keys()[0]
            stakeholder = fnamedict[fn]
        elif fn in nicknames:
            #look for nickname match
            stakeholder = 'NoFirstNameMatch' #set stakeholder to nomatch is default, override if you find a nickname match
            for nicky in nicknames[fn]:
                #see if any of the nicknames is in the fnamedict
                if nicky in fnamedict:
                    stakeholder = fnamedict[nicky]
                    break
        else:
            stakeholder = 'NOMATCH'
    else:
        stakeholder = 'NoLastNameMatch'
    return stakeholder
def getSupplierID(name):
    #get supplier with min edit distance.  If there is an exact match, distance s/b 0
                mindist = 10000
                #results = {}
                for k in suppliers.keys():
                    #dist = editdistance.eval(line[int(ru['InputColNo'])].lower(),k.lower())
                    dist = editdistance.eval(name.lower(),k.lower())
                    #results[k] = dist
                    if dist == 0:
                        minkey = k
                        break
                    #results[k] = dist
                    if dist < mindist:
                        mindist = dist
                        minkey = k
                return suppliers[minkey], dist, mindist, minkey
                
#process input files

#def processFiles(foldername):
            
#process user list       
users = {}

#if using AD user list
##usersfilename = os.path.join(foldername,'MultcoUsers.csv')
###with open('h:/JaggaerDC/MultcoUsers.csv','r') as u:
##with open(usersfilename,'r') as u:
##    for line in csv.reader(u):
##        namein = line[0].split()
##        lname = namein[0].lower()
##        fname = ''
##        for w in range(1,len(namein)):
##            if len(namein[w]) > 1:
##                fname = fname + namein[w].lower()
##        if lname in users:
##            namedict = users[lname]
##            namedict[fname] = line[4]
##            users[lname] = namedict
##        else:
##            x = {}
##            x[fname] = line[4]
##            users[lname] = x      

#if using Jaggaer user list
usersfilename = os.path.join(foldername, 'JaggaerUsers.csv')
with open(usersfilename,'r') as u:
    for line in csv.reader(u):
        fname = line[1].lower()
        lname = line[2].lower()
        if lname in users:
            namedict = users[lname]
            namedict[fname] = line[0]
            users[lname] = namedict
        else:
            x = {}
            x[fname] = line[0]
            users[lname] = x     
        

#process nickname list
nicknames = {}
nicknamesfilename = os.path.join(foldername,'nicknames.csv')
#with open('h:/JaggaerDC/nicknames.csv','r') as nickname:
with open(nicknamesfilename,'r') as nickname:
    for line in csv.reader(nickname):
        fullname = line[0].lower()
        if fullname in nicknames:
            nnlist = nicknames[fullname]
            nnlist.append(line[1].lower())
            nicknames[fullname] = nnlist
        else:
            nnlist = []
            nnlist.append(line[1].lower())
            nicknames[fullname] = nnlist


ContractType = {}
contracttypefilename = os.path.join(foldername,'ContractType.csv')
#with open('h:/JaggaerDC/ContractType.csv','r') as ct:
with open(contracttypefilename,'r') as ct:
    
    for line in csv.reader(ct):
        ContractType[line[0]] = [line[1],line[2]]
    ct.close()

#status
status = {}
statusfilename = os.path.join(foldername,'status.csv')
#with open('h:/JaggaerDC/status.csv','r') as stat:
with open(statusfilename,'r') as stat:
    
    for line in csv.reader(stat):
        status[line[0]] = line[1]
    stat.close()

#suppliers
suppliers = {}
suppliersfilename = os.path.join(foldername,'suppliers.csv')
#with open('h:/JaggaerDC/suppliers.csv','r') as sup:
with open(suppliersfilename,'r') as sup:

    for line in csv.reader(sup):
        suppliers[line[0]] = line[1]
    sup.close()

#projects
project = {}
projectsfilename = os.path.join(foldername,'projects.csv')
with open(projectsfilename,'r') as proj:
    for line in csv.reader(proj):
        project[line[0]] = line[1]
    proj.close()

import os
import sys
import csv
from datetime import date
from datetime import timedelta

import contract_help as ch

def convert(filename,contnumb,expire,suffix, env):

    foldername = os.path.dirname(filename)

    if __name__ == '__main__':
        ContractNumber = int(raw_input('Enter starting contract number: '))
        ExpirationCutoff = raw_input('Enter number of days: ')
        ExpirationCutoff = int(ExpirationCutoff)
        NumberSuffix = raw_input('Enter text to append to the contract number or press enter to bypass: ')
        if NumberSuffix != '':
            NumberSuffix = '-' + NumberSuffix
    else:
        ContractNumber = contnumb
        ExpirationCutoff = expire
        NumberSuffix = suffix
        if NumberSuffix != '':
            NumberSuffix = '-' + NumberSuffix

    if env == 'Test':
        FirstPartyID = '10539771'
    else:
        FirstPartyID = '19281501'

    

    #f = open('h:/JaggaerDC/ContractData.csv','r')
    f = open(filename,'r')
    
    #fout = open('h:/JaggaerDC/ContractDataOut.csv','wb')
    outputfilename = os.path.join(foldername,'ContractDataOut.csv')
    fout = open(outputfilename,'wb')
    if __name__ == '__main__':
        r = open('h:/JaggaerDC/appdata/rules.csv','r')
    else:
        r = open('appdata/rules.csv','r')
    warnfilename = os.path.join(foldername,'warnings.csv')
    #warn = open('h:/JaggaerDC/warnings.csv','wb')
    warn = open(warnfilename,'wb')
    rules = []
    #Put expired rule into a settings file?  If there is anything else that can be put there, do so
    #maybe defaults for contract manager if it can't be identified from the rules.
    #ExpiredExclusionFilter = 

    #process rules - make into a list of dictionaries
    for line in csv.reader(r):
        
        rules.append(dict(SciFieldName=line[0],
                          Input=line[1],
                          InputColNo=line[2],
                          RuleType=line[3],
                          MapName=line[4],
                          DefaultValue=line[5],
                          TransformRule=line[6],
                          Header=line[10]))
    r.close()

    mywriter = csv.writer(fout, delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
    warningwriter = csv.writer(warn,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)

    #write the header
    lineout = []
    for ru in rules:
        lineout.append(ru['Header'])
    mywriter.writerow(lineout)

    warninglist = [] #put all the warnings in a list, then print out

    #setup variable to use in expiration date cutoff test
    now = date.today()
    yeardiff = timedelta(ExpirationCutoff)
    cutoff = now-yeardiff

    #get the column index for ProjectCode and ContractType from rules list - do outside of processing the input
    #file so the code is only executed once
    projectfound = False
    typefound = False
    for rx in rules:
        if rx['SciFieldName'] == 'ProjectCode':
            projindex = int(rx['InputColNo'])
            projectfound = True
            print projindex
        if rx['SciFieldName'] == 'Contract Type':
            typeindex = int(rx['InputColNo'])
            typefound = True
            print typeindex
        if projectfound and typefound:
            break        

    for line in csv.reader(f):
        lineout = []
        warning = []
        
        ####if expired more than 1 year ago, do not import
        expdate = line[10].split('/')
        expdatetest = date(int(expdate[2]),int(expdate[0]),int(expdate[1]))
        if expdatetest < cutoff:
            continue
        
    ##    if expdatetest < now:
    ##        diff = abs(now - expdatetest)
    ##        if diff.days > 365:
    ##            continue
        #####################

        #get project and contract type - it is used in the contract number, as well as being its own field
        projectcode = ch.project.get(line[projindex],'badkey')
        typecode = ch.ContractType.get(line[typeindex],['badkey','badkey'])[0]
        typeabbrev = ch.ContractType.get(line[typeindex],['badkey','badkey'])[1]
        #typecode = 'services'
        #typeabbrev = 'svc'
     
        for ru in rules:
            if ru['RuleType'] == 'transform':
                if ru['SciFieldName'] == 'Second PartyID':
                   SupplierID, dist, mindist, minkey = ch.getSupplierID(line[int(ru['InputColNo'])])
                   lineout.append(SupplierID)
                   if dist > 0:
                        warning.append('Vendor')
                        warning.append(line[0]) #Sap contract number
                        warning.append(number) #SciQuest contract number
                        warning.append(line[2]) #contact name
                        warning.append(line[int(ru['InputColNo'])]) #vendor name
                        warning.append(mindist)
                        warning.append(minkey)
                        warning.append('Exact match not found.  Closest match used.')
                        warninglist.append(warning)
                        #warningwriter.writerow(warnings)
                if ru['SciFieldName'] == 'Contract Number':
                    number = projectcode + '-' + typeabbrev + '-' + str(ContractNumber) + \
                    '-' + ch.getFY(line[9]) + NumberSuffix
                    lineout.append(number)
                    ContractNumber += 1
                elif ru['SciFieldName'] == 'StartDate' or ru['SciFieldName'] == 'EndDate':
                    lineout.append(ch.formatDate(line[int(ru['InputColNo'])])) #start date need to reformat
                    #print line[int(ru['InputColNo'])], formatDate(line[int(ru['InputColNo'])])
                elif ru['SciFieldName'] == 'ContractManagers':
                    manager,stakeholder = ch.getManagerStakeholder(line[6],line[8])
                    #if not either not = '', get userid from name
                    if manager != '':
                        manager_userid = ch.getUserID(manager)
                    if manager_userid == 'NOMATCH' or manager_userid == 'NoLastNameMatch':
                        #write warning
                        warning = []
                        warning.append('Manager')
                        warning.append(line[0])
                        warning.append(manager)
                        warning.append(manager_userid)
                        warninglist.append(warning)
                        lineout.append('')
                    else:
                        if manager == '':
                            lineout.append('')
                        else:
                            lineout.append(manager_userid)
                elif ru['SciFieldName'] == 'Stakeholders':
                    
                    if stakeholder != '':
                        stakeholder_userid = ch.getUserID(stakeholder)
                    #else:
                    #    stakeholder_userid = ''
                    if stakeholder_userid == 'NOMATCH' or stakeholder_userid == 'NoLastNameMatch':
                        #write warning
                        warning = []
                        warning.append('Stakeholder')
                        warning.append(line[0])
                        warning.append(stakeholder)
                        warning.append(stakeholder_userid)
                        warninglist.append(warning)
                        lineout.append('')
                    else:
                        if stakeholder == '':
                            lineout.append('')
                        else:
                            lineout.append(stakeholder_userid)
                #else:
                #    lineout.append(line[int(ru['InputColNo'])]) #end date need to reformat
            elif ru['RuleType'] == 'default':
                lineout.append(ru['DefaultValue'])
            elif ru['RuleType'] == 'map':
                if ru['MapName'] == 'ContractType':
                    #index = line[int(ru['InputColNo'])]
                    #lineout.append(ch.ContractType.get(typeindex,['badkey','badkey'])[0])
                    lineout.append(typecode)
                    #lineout.append('testmap')
                elif ru['MapName'] == 'status':
                    index = line[int(ru['InputColNo'])]
                    lineout.append(ch.status.get(index,'badkey'))
                    #lineout.append('testmap')
                elif ru['MapName'] == 'project':
                    lineout.append(projectcode)
                elif ru['MapName'] == 'Env':
                    lineout.append(FirstPartyID)
            elif ru['RuleType'] == 'copy':
                lineout.append(line[int(ru['InputColNo'])])
                
        mywriter.writerow(lineout)
    #write warnings
    for wa in warninglist:
        warningline = []
        for item in wa:
            warningline.append(item)
        warningwriter.writerow(warningline)
            
        
    f.close()
    fout.close()
    warn.close()

if __name__ == '__main__':
    convert('h:\JaggaerDC\ContractData.csv')

    


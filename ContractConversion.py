import os
import sys
import csv
from datetime import date
from datetime import timedelta
import GetConfig as g
import contract_help as ch

def convert(filename,contnumb,expire,suffix,env):

    #foldername = os.path.dirname(filename)

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

##    if env == 'Test':
##        FirstPartyID = '1000105838'
##    else:
##        FirstPartyID = '19281501'

#need to mod to pull the contract manager from the input filename
#so rules will need to be changed
#should also validate that the ad ids from srm are correct - some of
#them don't have names associated which seems odd.

#adding a comment to test github integration.

    FirstPartyID = g.parmdict['FirstPartyId']
    iodir = g.parmdict['IOFileDirectory']
    appdir = g.parmdict['AppDataDirectory']
    logdir = g.parmdict['LogFileDirectory']

    #f = open('h:/JaggaerDC/ContractData.csv','r')
    #f = open(filename,'r')
    f = open(g.parmdict['HeaderDataFilePath'],'r')

    #this should probably go in the helper script to be consistent
    #used to get file crossreferences
    filexrefdict = {}
    with open(os.path.join(iodir,'ContractFileData.csv'),'r') as filexref:
        for line in csv.reader(filexref):
            filexrefdict[line[0]] = [line[1],line[2]]

    #fout = open('h:/JaggaerDC/ContractDataOut.csv','wb')
    outputfilename = os.path.join(iodir,'ContractDataOut.csv')
    fout = open(outputfilename,'wb')
    #if __name__ == '__main__':
    #    r = open('AppData/rules.csv','r')
    #else:
    #    r = open('AppData/rules.csv','r')
    r = open(os.path.join(appdir,'rules.csv'),'r')

    #separate file for missing suppliers
    missingfilename = os.path.join(iodir,'MissingSuppliers.csv')
    miss = open(missingfilename,'wb')


    warnfilename = os.path.join(logdir,'warnings.csv')
    #warn = open('h:/JaggaerDC/warnings.csv','wb')
    warn = open(warnfilename,'wb')
    rules = []
    colnumlookup = {}
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
        #create dictionary of field names and input col no
        if line[2] <> '':
            colnumlookup[line[0]] = int(line[2])

    r.close()

    mywriter = csv.writer(fout, delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
    warningwriter = csv.writer(warn,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
    misswriter = csv.writer(miss,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)

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

    #Get column indexes for various input columns
    projindex = colnumlookup['ProjectCode']
    typeindex = colnumlookup['ContractType']
    startindex = colnumlookup['StartDate']
    endindex = colnumlookup['EndDate']
    mgrindex = colnumlookup['ContractManagers']
    stakeindex = colnumlookup['Stakeholders']
    contractnameindex = colnumlookup['ContractName']
    sapnumberindex = colnumlookup['*SAPNumber']
    suppliernumberindex = colnumlookup['SecondPartyId']
    suppliernameindex = suppliernumberindex + 1

    for line in csv.reader(f):
        #skip the header line if there is one
        #shouldn't hardcode the column header but challenge is there might or might not be a header line
        #so can't just skip the first line
        if line[0] == 'Contract_Name':
            continue
        lineout = []
        warning = []

        #if expired before the number of days before the current date
        #specified, do not import

        expdate = line[endindex].split('/')
        expdatetest = date(int(expdate[2]),int(expdate[0]),int(expdate[1]))
        if expdatetest < cutoff:
            continue

        #get project and contract type - it is used in the contract number, as well as being its own field
        projectcode = ch.project.get(line[projindex],'badkey')
        typecode = ch.ContractType.get(line[typeindex],['badkey','badkey'])[0]
        typeabbrev = ch.ContractType.get(line[typeindex],['badkey','badkey'])[1]
        sapnumber = line[sapnumberindex]
        maindoc = filexrefdict.get(sapnumber,['',''])[0]
        attachments = filexrefdict.get(sapnumber,['',''])[1]
        #typecode = 'services'
        #typeabbrev = 'svc'

        for ru in rules:
            if ru['RuleType'] == 'transform':
                if ru['SciFieldName'] == 'SecondPartyId':
                #this one needs work - eventually should compare on SAP Vendor ID
                #for now, using a default supplier and we will pull in the correct ones
                #for testing the extract for workday
                    #if env == 'Test':
                    #   lineout.append('1000192800')
                    #else:
                   SupplierID = ch.getSupplierID(line[suppliernumberindex])
                   if SupplierID == 'VendorNumberNotFound':
                       warninglist.append(ch.writeWarning('SupplierID',line[contractnameindex],line[sapnumberindex],line[suppliernameindex] + ':' + \
                       line[suppliernumberindex],'SAP Vendor number not found'))
                       lineout.append('')
                   else:
                       lineout.append(SupplierID)

                if ru['SciFieldName'] == 'ContractNumber':
                    number = projectcode + '-' + typeabbrev + '-' + str(ContractNumber) + \
                    '-' + ch.getFY(line[startindex]) + NumberSuffix
                    lineout.append(number)
                    ContractNumber += 1
                elif ru['SciFieldName'] == 'StartDate' or ru['SciFieldName'] == 'EndDate':
                    lineout.append(ch.formatDate(line[int(ru['InputColNo'])])) #start date need to reformat
                    #print line[int(ru['InputColNo'])], formatDate(line[int(ru['InputColNo'])])
##                elif ru['SciFieldName'] == 'ContractManagers':
##                    #manager, stakeholder = ch.getManagerStakeholder(line[line[stakeindex], mgrindex])
##                    #above line calls a function that does various defaulting and switching around depending on
##                    #which fields between owner and support person are populated in SAP
##                    #for now removing this call in favor of defaulting a manager based on department or just leaving blank.
##
##                    manager = line[mgrindex]
##                    if manager != '':
##                        manager_userid = ch.getUserID(manager)
##                        if manager_userid == 'NOMATCH':
##                            #write warning
##                            warninglist.append(ch.writeWarning('Manager',line[contractnameindex],line[sapnumberindex],manager,manager_userid))
##                            lineout.append('')
##                        else:
##                            lineout.append(manager_userid)
##                    else:
##                        warninglist.append(ch.writeWarning('Manager',line[contractnameindex],line[sapnumberindex],'','No contract manager specified'))
##                        lineout.append('')
                elif ru['SciFieldName'] == 'Stakeholders':
                    stakeholder = line[stakeindex]
                    if stakeholder != '':
                        stakeholder_userid = ch.getUserID(stakeholder)
                        if stakeholder_userid == 'NOMATCH':
                            #write warning
                            warninglist.append(ch.writeWarning('Stakeholder',line[contractnameindex],line[sapnumberindex],stakeholder,stakeholder_userid))
                            lineout.append('')
                        else:
                            lineout.append(stakeholder_userid)
                    else:
                        warninglist.append(ch.writeWarning('Stakeholder',line[contractnameindex],line[sapnumberindex],'','No stakeholder specified'))
                        lineout.append('')
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
                if ru['SciFieldName'] == 'ContractName':
                    if line[int(ru['InputColNo'])] == '':
                        lineout.append('Unnamed Contract')
                    else:
                        lineout.append(line[int(ru['InputColNo'])])
                else:
                    lineout.append(line[int(ru['InputColNo'])])
            elif ru['RuleType'] == 'lookup':
                if ru['SciFieldName'] == 'MainDocumentAttachment':
                    lineout.append(maindoc)
                else:
                    if attachments == 'NA':
                        attachments = ''
                    lineout.append(attachments)
        if SupplierID == 'VendorNumberNotFound':
            misswriter.writerow(line)
        else:
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
    miss.close()

if __name__ == '__main__':
    convert('h:\\JaggaerDC\\ContractData.csv','','','','Test')

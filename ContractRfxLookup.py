import os
import csv

f = open('h:/JaggaerDC/ContractData.csv','r')
fout = open('h:/JaggaerDC/ContractRfxLkup.csv','wb')
mywriter = csv.writer(fout, delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)

for line in csv.reader(f):
    lineout = []
    lineout.append(line[0])     #contract number
    lineout.append(line[17])    #associated RFx Numbers
    mywriter.writerow(lineout)    


f.close()
fout.close()

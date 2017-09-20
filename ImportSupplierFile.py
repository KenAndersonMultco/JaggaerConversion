import csv
import os


def import(filename):

    #rename previous file
    #os.rename(src,dst)

    if not os.path.exists('.\AppData\SupplierArchive'):
        os.makedirs('.\AppData\SupplierArchive')
    else:
        for fname in os.listdir('.\AppData\SupplierArchive')


    if os.getcwd() == 'C:\Python27\Scripts\MyScripts':
        foldername = 'H:\JaggaerDC\AppData'
    else:
        foldername = 'AppData'
    sfilename = os.path.join(foldername,'suppliers.csv')
    sfile = open(sfilename,'wb')
    swriter = csv.writer(sfile, delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
    
    with open(filename,'r') as s:
        for line in csv.reader(s):
            supplier = []
            supplier.append(line[0])
            supplier.append(line[1])
            supplier.append(line[6])
            supplier.append(line[11])
            supplier.append(line[18])
            swriter.writerow(supplier)

if __name__ == '__main__':
    import('h:\JaggaerDC\SupplierData\')
            

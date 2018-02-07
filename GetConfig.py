import xml.etree.ElementTree as ET
parmdict = {}
tree = ET.parse('//nas3/CW-IT/Projects/GG/JaggaerConversion/AppData/config.xml')
root = tree.getroot()
for child in root:
    parmdict[child.tag] = child.text

from tkinter import *
from tkinter.filedialog import askopenfilename
from guiStreams import redirectedGuiFunc
from ContractConversion import convert
fields = 'Starting Number', 'Expiration Lookback (in days)','Number Suffix'
#snum = 1
#exp = 365
#num = ''

def makeform(root, fields):
    entries = []
    for field in fields:
        row = Frame(root)                           # make a new row
        lab = Label(row, width=25, text=field, anchor = E)       # add label, entry
        ent = Entry(row)
        row.pack(side=TOP, fill=X)                  # pack row on top
        lab.pack(side=LEFT)
        #ent.pack(side=RIGHT, expand=YES, fill=X)    # grow horizontal
        ent.pack(side=LEFT,padx=10)  #do not grow horizontally
        entries.append(ent)
    return entries

def fetch(entries, var):
    snum = int(entries[0].get())
    exp = int(entries[1].get())
    num = entries[2].get()
    env = var.get()
    getfilenamerd(snum, exp, num, env)
    
    


def getfilename(snum, exp, num, env):

    filename = askopenfilename()
    print filename
    #get other input - create toplevel window to get input
    #win1 = Toplevel()
    
    #win1.bind('<Return>', (lambda event: fetch(ents)))
    #fetcher = Button(win1, text = 'Fetch',command=(lambda: fetch(ents))).pack(side=LEFT)
    #finish = Button(fr, text = 'Done', command=(lambda: fetch(ents))).pack(side=LEFT)
    
    
    #for test print entries
    print snum, exp, num
    print env
    
    convert(filename,snum,exp,num,env)
    print '\nI''m done'
    

def getfilenamerd(snum, exp, num, env):
    redirectedGuiFunc(getfilename, snum, exp, num, env)

root = Tk()
fr = Frame(root).pack()
ents = makeform(fr, fields) #attach form to
Label(fr,text='Choose Environment').pack(side=TOP, anchor=NW)
var = StringVar()
Radiobutton(fr,text = 'Test', variable = var, value='Test').pack(anchor=NW)
Radiobutton(fr,text = 'Prod', variable = var, value='Prod').pack(anchor=NW)
var.set(' ')
action = Button(fr,text='GetFile',command = (lambda: fetch(ents, var))).pack()


#quitme = Button(fr,text='Quit',command=root.quit) #doesn't work in IDLE
quitme = Button(fr,text='Quit',command=root.destroy)
quitme.pack()


root.mainloop()

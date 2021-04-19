from tkinter import Tk, messagebox, Label, Button, Menu, Entry, StringVar
from webserv import cardVerify
from configparser import ConfigParser, ExtendedInterpolation
import webbrowser, os, copy

config = ConfigParser(interpolation=ExtendedInterpolation())
config.read('config.ini')

msg = config['MESSAGE']['About']
bText = config['MESSAGE']['Button']
lText = config['MESSAGE']['Label']
bgcolor = config['APP']['Background']
fcolor = config['FONT']['Color']
fsize = config['FONT']['Size']
fname = config['FONT']['Type']

labelFont = (fname, fsize)
messageFont = fname + " " + str(fsize)

app = Tk()
app.option_add('*Dialog.msg.font', messageFont)

def get_verify(e=False):
    cardNumber = patron_text.get()
    message = cardVerify(cardNumber)
    if message['status'] == "OK":
        messagebox.showinfo(title="Update", message=message['message'])
    else:
        messagebox.showerror(title="Error", message=message['message'], icon='error')

def ContinuetoVerify(e=False):
    MsgBox = messagebox.askquestion('About',msg + " Continue?",icon = 'warning')
    if MsgBox == 'yes':
        get_verify()
    else:
       app.destroy()      

def openWeb(myURL):
    webbrowser.open(myURL)

def openMsgBx(Title, Message):
    messagebox.showinfo(title=Title, message=Message)

#Menu
if config['APP'].getboolean('Menu'):
    menubar = Menu(app)
    for mkey in config['MENU']:
        mtitle = mkey.title()
        mlist = config['MENU'][mkey].split()
        tempMenu = Menu(menubar, tearoff=0)
        i = 0
        for subKey in config[mtitle]:
            tact = config[mtitle][subKey]
            if 'msg' in mlist[i]:
                ttitle = subKey.title()
                tempMenu.add_command(label=ttitle, command=lambda: openMsgBx(ttitle, tact))
            elif 'url' in mlist[i]:
                ttitle = subKey.title()
                tempMenu.add_command(label=ttitle, command=lambda: openWeb(tact))
            i = i + 1
        menubar.add_cascade(label=mtitle, menu=tempMenu)
    app.configure(menu=menubar)

# Patron Card Number Widget
patron_text = StringVar()
Label(app, bg=bgcolor, fg=fcolor, text=lText, font=labelFont).pack(pady=20)
cNumber = Entry(app, textvariable=patron_text, font=messageFont)
cNumber.focus_set()
cNumber.pack()
Button(app, text=bText, command = ContinuetoVerify, padx=10, pady=5).pack(pady=10)

cwd = os.getcwd()
cwd = cwd + '/appicon.ico'
app.iconbitmap(cwd)
app.title('Patron Defilter Request')
app.geometry('250x160')
app.configure(background=bgcolor)
app.bind('<Return>',ContinuetoVerify)

app.mainloop()
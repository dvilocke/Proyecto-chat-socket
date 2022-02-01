from socket import MsgFlag
from tkinter import *
'''
Apuntes:
Frame: marco que permite agrupar diferentes widgets.
'''
class UI(Frame):
    def __init__(self,user,master, socket):
        Frame.__init__(self, master)
        self.config(cursor='pirate', bd=15)
        self.conn = socket
        self.user = user
        self.master = master
        self.grid()
        self.create_widgets()


    def send_server(self):
        self.conn.send(self.text_ent.get().encode())
        self.text_ent.delete(0,END)

    def to_write(self,msg):
        self.text.insert(END, f'{msg}\n')

    def exit_user(self):
        self.user.exit = True
    
    def create_widgets(self):
        #Label
        self.label = Label(self, text='creator: Ing Miguel Echeverry')

        #we create the text area
        self.text = Text(self, height=20, width=40)
        self.scroll = Scrollbar(self, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scroll.set)

        #for the user to type
        self.send_text = StringVar()
        self.text_ent = Entry(self, textvariable=self.send_text)

        #buttons
        self.buton_send = Button(self,text='Send', command=self.send_server)
        self.buton_exit = Button(self,text='Exit',command=self.exit_user)
        
        #include in frame
        self.label.grid(row=0, column=0)
        self.text.grid(row=1, column=0, columnspan=2)
        self.scroll.grid(row=1, column=2, sticky=N+S)
        self.text_ent.grid(row=2, column=0, columnspan=2, sticky=W+E)
        self.buton_send.grid(row=3, column=0)
        self.buton_exit.grid(row=3,column=1)

root = Tk()
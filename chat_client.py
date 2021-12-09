import socket
from sys import tracebacklimit
import threading
import tkinter
import tkinter.scrolledtext

from tkinter import simpledialog
from typing import TYPE_CHECKING

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9090

class Client:

    def __init__(self, host, port) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        msg = tkinter.Tk()
        msg.withdraw() 

        self.username = simpledialog.askstring("Username", "Please choose a username", parent=msg)

        self.gui_done = False # tells that the gui is not yet built
        self.running = True # The server status

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()
    
    def gui_loop(self): 
        """The GUI daemon to keep GUI up"""
        #The frontend is built here 
        self.win = tkinter.Tk()
        self.win.configure(bg="lightgray")

        #main window heading
        self.chat_label = tkinter.Label(self.win, text="Babel Chat", bg='lightgray')
        self.chat_label.config(font=("Calibri", 12))
        self.chat_label.pack(padx=25, pady=5)
        #The visible text area
        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=25, pady=5)
        self.text_area.config(state='disabled')
        #Messaging area
        self.msg_label = tkinter.Label(self.win, text="Message", bg='lightgray')
        self.msg_label.config(font=("Calibri", 12))
        self.msg_label.pack(padx=25, pady=5)
        #input area
        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=25,pady=5)

        self.send_button = tkinter.Button(sle)



    def write(self):
        pass
    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):

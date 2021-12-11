import socket
from tkinter.constants import SEPARATOR
import boto3
import os
import tqdm
import threading
import tkinter
import tkinter.scrolledtext

from tkinter import simpledialog

SEPARATOR="<SEPARATOR>"
BUFFER_SIZE = 1024 * 4


HOST =socket.gethostbyname(socket.gethostname())
PORT = 9091
translate = boto3.client(service_name='translate', region_name='ap-south-1', use_ssl=True)
file = open("languages.txt", "r")
lang_dict={}
for line in file:
    parts=line[:-1].split('\t')
    lang_dict[parts[0]]=parts[1]



class Client:

    def __init__(self, host, port) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(host,port)
        self.sock.connect((host, port))

        msg = tkinter.Tk()
        msg.withdraw() 

        self.username = "ngon"#simpledialog.askstring("Username", "Please choose a username", parent=msg)
        #user_lang=simpledialog.askstring("Language", "Please choose a Language", parent=msg)
        self.langauge ="en"  #lang_dict[user_lang]
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
        self.chat_label = tkinter.Label(self.win, text="Babel Chat \U0001F41F", bg='lightgray')
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=25, pady=5)
        #The visible text area
        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=25, pady=5)
        self.text_area.config(state='disabled')
        #Messaging area
        self.msg_label = tkinter.Label(self.win, text="Message", bg='lightgray')
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.pack(padx=25, pady=5)
        #input area
        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=25,pady=5)

        self.send_button = tkinter.Button(self.win, text="Send", command=self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=25, pady=5)
        
        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop) # When the window is closed complete destruction of the chat application
        self.win.mainloop()


    def sendall(self,data,flag=0):
        sent=self.sock.send(data,flag)
        if sent>0:
            return self.sendall(data[sent:],flag)
        else:
            return None


    def file_send(self):
        filesize = os.path.getsize(self.filename)
        self.sock.send(f">> {self.filename}{SEPARATOR}{filesize}".encode("utf-8"))
        with open(self.filename,"rb") as f:
            while True:
                # read the bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    # file transmitting is done
                    break
                # we use sendall to assure transimission in 
                # busy networks
                self.sendall(bytes_read)
                # update the progress bar

    def file_receive(self):
        pass

    def write(self):
        """Writes your message into the area and deletes it after its sent."""
        message = f"{self.username}: {self.input_area.get('1.0', 'end')}"
        str = self.input_area.get('1.0', 'end')
        if str[0:2] == '>>':
            print('lol')
            self.filename=str[3:-1]
            self.file_send()
            print("file has been sent")
            fin=f"{self.username} has sent the file {self.filename}"
            self.sock.send(fin.encode("utf-8"))
        else:
            self.sock.send(message.encode("utf-8"))

        self.input_area.delete('1.0', 'end')

    def stop(self):
        """"stops the process when window is closed."""
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try: 
                message = self.sock.recv(1024).decode('utf-8')
                if message == "USERNAME":
                    self.sock.send(self.username.encode('utf-8'))
                else: 
                    message = translate.translate_text(Text=message, SourceLanguageCode="auto", TargetLanguageCode=self.langauge)
                    message=message['TranslatedText']
                    if self.gui_done: #makes sure our building of GUI is done
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message) #append the message at the end
                        self.text_area.yview('end') #scroll your view along with messages
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                self.sock.close()
                break

client = Client(HOST, PORT)

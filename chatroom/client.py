import tkinter
import socket

from tkinter import *
from threading import Thread


def receive():
    while True:
        
        try:
            msg = s.recv(1024).decode("utf8")
            if msg == '#quit':
                print('msg was quit')
                s.close()
                window.quit()
                exit()
            else:
                msg_list.insert(tkinter.END, msg)
        except Exception as e:
            print(f'There was an error: {e}')
            print(e.with_traceback)
            return False
        exit()


def send():
    msg = my_msg.get()
    my_msg.set("")
    s.send(bytes(msg, "utf8"))
    if msg == "#quit":
        on_closing()


def on_closing():
    s.close()
    window.quit()


window = Tk()

window.title('Chat Room App')
window.configure(bg='green')

message_frame = Frame(window, height=100, width=100, bg='blue')
message_frame.pack()
my_msg = StringVar()
my_msg.set("")

scroll_bar = Scrollbar(message_frame)
msg_list = Listbox(message_frame, height=15, width=100,
                   bg='white', yscrollcommand=scroll_bar.set)
scroll_bar.pack(side=RIGHT, fill=Y)
msg_list.pack(side=LEFT, fill=BOTH)
msg_list.pack()

label = Label(window, text="Enter a message",
              fg='black', font='Aeria', bg='grey')
label.pack()

entry_field = Entry(window, textvariable=my_msg, fg='black', width=50)
entry_field.pack()

send_button = Button(window, text="Send", font='Aerial',
                     fg='blue', command=send)
send_button.pack()
quit_button = Button(window, text='Quit', font='Aerial',
                     fg='white', command=on_closing)
quit_button.pack()


Host = '127.0.0.1'
Port = 8080
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((Host, Port))

receive_Thread = Thread(target=receive)

receive_Thread.start()

mainloop()

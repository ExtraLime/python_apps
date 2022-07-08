from re import sub
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import tkinter
from pygame import mixer

mixer.init()

def play_music():
    try:
        paused
    except:        
        try:
            mixer.music.load(filename)
            mixer.music.play()
        except Exception as e:
            messagebox.showerror("Error",'File cannot be played')
            print('File Cannot Be Played')
    else:
        mixer.music.unpause()
    
def pause_music():
    try:
        global paused
        paused=True
        mixer.music.pause()
    except Exception as e:
        pass

def stop_music():
    mixer.music.stop()
    
def set_volume(value):
    volume = int(value)/100
    mixer.music.set_volume(volume)
    
def browse_files():
    global filename
    filename = filedialog.askopenfile()
    
def help_me():
    messagebox.showinfo("How amazing it is", 'Truly')
    
window = Tk()

window.geometry('300x300')
window.title('Python Music Player')
menubar = Menu(window)
submenu = Menu(menubar,tearoff=0)
submenu1 = Menu(menubar,tearoff=0)

window.config(menu=menubar)

menubar.add_cascade(label='File',menu=submenu)
submenu.add_command(label="Open",command=browse_files)
submenu.add_command(label="Exit",command=window.destroy)

menubar.add_cascade(label='About Us',menu=submenu1)
submenu1.add_command(label="Help",command=help_me)



textLabel = Label(window, text="This is a Play Button")
textLabel.pack()

frame = Frame(window)
frame.pack(padx=10, pady=10)

play_photo = PhotoImage(file='index.png')
playbutton = Button(frame, image=play_photo, command=play_music)
playbutton.pack(side=LEFT)

stop_photo = PhotoImage(file='stop.png',height=100,width=100)
stop_button = Button(frame, image=stop_photo, command=stop_music)
stop_button.pack(side=LEFT)
pause_photo = PhotoImage(file='wm-pause.png')
pause_button = Button(frame,image=pause_photo,command=pause_music)
pause_button.pack(side=LEFT)

scale = Scale(window, from_=0,to=100,orient=HORIZONTAL,command=set_volume)
scale.set(70)
scale.pack()


window.mainloop()
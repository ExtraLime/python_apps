#!/usr/bin/env python3
from turtle import title
from pytube import YouTube
from tkinter import filedialog
from tkinter import ttk
from tkinter import *
import re
import threading

class Application:
    def __init__(self,root):
        self.root = root
        self.root.grid_rowconfigure(0,weight=2)    
        self.root.grid_columnconfigure(0,weight=1)
        self.root.config(bg="#CD5C5C")
        
        top_label = Label(self.root,text="YouTube Dowload Manager",fg='orange', font=('Times',70))
        top_label.grid(pady=(0,10))
        
        link_label = Label(self.root, text='Please Paste a YouTube Video Link Below',font=('Times',30))
        
        link_label.grid(pady=(0,20))
        
        self.youtubeEntryVar = StringVar()
        self.youtubeEntry = Entry(self.root,width=70,textvariable=self.youtubeEntryVar, font=('Times',25))
        self.youtubeEntry.grid(pady=(0,15),ipady=2)
        
        self.youtubeEntryError = Label(self.root, text="", font=('Times',20))
        self.youtubeEntryError.grid(pady=(0,8))
        
        self.youtubeFileSaveLabel = Label(self.root,text='Choose Directory',font=('Times",30'))
        self.youtubeFileSaveLabel.grid()
        
        self.youtubeFileDirectoryButton = Button(self.root, text="Directory",font=('Times',15),command=self.openDirectory)
        self.youtubeFileDirectoryButton.grid(pady=(10,3))
        
        self.fileLocationLabel = Label(self.root,text="",font=('Times',25))
        self.fileLocationLabel.grid()
        
        self.youtubeChooseLabel = Label(self.root, text='Choose Download Type',font=('Times',25))
        self.youtubeChooseLabel.grid()
        
        self.downloadChoices = [('Audio mp3',1),('Video mp4',2)]
        self.choiceVar = StringVar()
        self.choiceVar.set(1)
        
        for text,mode in self.downloadChoices:
            self.youtubeChoices = Radiobutton(self.root,text=text, font=('Times',15), variable=self.choiceVar, value=mode)
            self.youtubeChoices.grid()
            
        self.downloadButton = Button(self.root, text="Download",width=10,font=('Times",15'),command=self.checkyoutubelink)
        self.downloadButton.grid(pady=(30,5))
        
    def checkyoutubelink(self):
        
        self.matchyoutubelink = re.match("^https://www.youtube.com/.",self.youtubeEntryVar.get())
        if not self.matchyoutubelink:
            self.youtubeEntryError.config(text='Invalid Youtube Link',fg='red')
        elif not self.openDirectory:
            self.fileLocationLabel.config(text='Please select a directory to save the file',fg='red')
        elif self.matchyoutubelink and self.openDirectory:
            self.downloadWindow()
        
    def downloadWindow(self):
        
        self.newWindow = Toplevel(self.root)
        self.newWindow.title('YouTube Downloader')
        w, h = self.newWindow.winfo_screenwidth(), self.newWindow.winfo_screenheight()
        self.newWindow.geometry("%dx%d+0+0" % (w, h))
        self.newWindow.grid_rowconfigure(0,weight=0)
        self.newWindow.grid_columnconfigure(0,weight=1)
        
        self.root.withdraw()
        
        self.app = SecondApp(self.newWindow,self.youtubeEntryVar.get(),self.dir_name,self.choiceVar.get())
            
        
    def openDirectory(self):
        self.dir_name = filedialog.askdirectory()
        
        if(len(self.dir_name)>0):
            self.fileLocationLabel.config(text=self.dir_name, fg='black')
            return True
        else:
            self.fileLocationLabel.config(text="Please choose a valid Directory", fg='red')
            
class SecondApp:
    def __init__(self,downloadWindow,youtubelink,dir_name,choices):
        self.downloadWindow = downloadWindow
        self.youtubelink = youtubelink
        self.dir_name = dir_name
        self.choices = choices
        self.yt = YouTube(self.youtubelink)
        
        
        if choices == "1":
            
            self.video_type = self.yt.streams.filter(only_audio=True).first()
            self.MaxFileSize = self.video_type.filesize
            
        if choices == '2':
            self.video_type = self.yt.streams.get_highest_resolution()
            self.MaxFileSize = self.video_type.filesize
            
        self.loadingLabel = Label(self.downloadWindow,text='Downloading in Progress',font=('Times',40))
        self.loadingLabel.grid(pady=(100,0))
        self.loadingPercent = Label(self.downloadWindow, text="0",fg='green',font=("Times",40))
        self.loadingPercent.grid(pady=(50,0))
        
        self.progressBar = ttk.Progressbar(self.downloadWindow,length=500,orient='horizontal',mode='indeterminate')
        self.progressBar.grid(pady=(50,0))
        self.progressBar.start()
        
        threading.Thread(target=self.yt.register_on_progress_callback(self.show_progress)).start()
        
        threading.Thread(target=self.downloadFile).start()
        
    def downloadFile(self):
        if self.choices=='1':
            self.yt.streams.filter(only_audio=True).first().download(self.dir_name)
        if self.choices == '2':
            self.yt.streams.get_highest_resolution().download(self.dir_name)
    
    def show_progress(self,stream=None,chunks=None, bytes_remaining=None):
        print(stream)
        print(bytes_remaining)
        print(self.MaxFileSize)
        self.percentCount = round(float(100 -(100*(bytes_remaining/self.MaxFileSize))),2)
        print(self.percentCount)
        
        
        
        print(self.percentCount)
        if self.percentCount <100:
            print(self.percentCount)
            self.loadingPercent.config(text=self.percentCount)
        else:
            self.loadingPercent.config(text='100%')
            self.progressBar.stop()
            self.loadingLabel.grid_forget()
            self.progressBar.grid_forget()
            
            self.downloadFinished = Label(self.downloadWindow, text='Download Complete',font=("Times",30))
            self.downloadFinished.grid(pady=(150,0))
            
            self.downloadedFileName = Label(self.downloadWindow, text=self.yt.title,font=("Times",30))
            self.downloadedFileName.grid(pady=(50,0))
            
            MB = float("%0.2f" % (self.MaxFileSize/1000000))
            self.downloadFileSize = Label(self.downloadWindow, text=str(MB)+'MB',font=("Times",30))
            self.downloadFileSize.grid(pady=(50,0))
        
            
            
         

if __name__=='__main__':

    window = Tk()
    window.title('YouTube Downloader')
    w, h = window.winfo_screenwidth(), window.winfo_screenheight()
    window.geometry("%dx%d+0+0" % (w, h))
    
    app = Application(window)    
    mainloop()

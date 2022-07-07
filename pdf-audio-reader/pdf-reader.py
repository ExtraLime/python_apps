from tkinter import *
from tkinter import *
from tkinter import filedialog
import PyPDF2
import pyttsx3

def extract_text():
    file = filedialog.askopenfile(parent=root, mode='rb',title="Choose a PDF File")
    if file != None:
        pdfReader = PyPDF2.PdfFileReader(file)
        global text_extracted
        text_extracted = ""
        for pageNum in range(pdfReader.numPages):
            pageObject = pdfReader.getPage(pageNum)
            text_extracted += pageObject.extractText()
        file.close()

def speak_text():
    global rate
    global male
    global female
    print(rate.get())
    rate = int(rate['text'])
    engine.setProperty('rate',rate)
    male = int(male.get())
    female = int(female.get())

    '''
    This whole section is too much all we need to do is
    check if female voice == 1 and male voice == 0
    '''
    if male == female:
        engine.setProperty('voice','m1')
    elif female == 1 and male==0:
        engine.setProperty('voice','f1')
    else:
        engine.setProperty('voice','m1')
        
    engine.say(text_extracted)
    engine.runAndWait()
    
def stop_speaking():
    engine.stop()
    
def Application(root):
    root.geometry(f'{700}x{600}')  # 700x600 size windows
    root.resizable(width=False, height=False)
    root.title("Read My PDF")
    root.configure(bg='black')
    global rate, male, female
    print(rate)
    frame1 = Frame(root, width=500, height=200, bg='indigo')

    frame2 = Frame(root, width=500, height=450, bg='black')

    frame1.pack(side=TOP, fill='both')
    frame2.pack(side=TOP, fill='y')

    # frame1 widgets
    name1 = Label(frame1, text='PDF to AUDIO', fg='grey',
                  bg='lime', font="Arial 28 bold")
    name1.pack()

    name2 = Label(frame1, text='Listen to your PDF',
                  fg='grey', bg='lime', font="Arial 28 bold")
    name2.pack()

    # frame2 Widgets

    btn = Button(frame2, text='Select PDF', activeforeground='pink',
                 command=extract_text, padx=70, pady=10, fg='white', bg='black', font='Arial 12')
    btn.grid(row=0, pady=20, columnspan=2)

    rate_text = Label(frame2, text='Enter Rate of Speach',
                      fg='black', bg='aqua', font='Arial 12')
    rate_text.grid(row=1, column=0, pady=15, padx=0, sticky=W)

    rate = Entry(frame2, text='100', fg='white', bg='black', font='Arial 14')
    rate.grid(row=1, column=1, padx=30, pady=15, sticky=W)

    voice_text = Label(frame2, text='Select Voice',
                       fg='black', bg='aqua', font="Arial 12")
    voice_text.grid(row=2, column=0, pady=15, padx=0, sticky=E)

    male = IntVar()
    maleOpt = Checkbutton(frame2, text='Male', bg='blue',
                          variable=male, onvalue=1, offvalue=0)
    maleOpt.grid(row=2, column=1, padx=30, pady=0, sticky=W)

    female = IntVar()
    femaleOpt = Checkbutton(frame2, text='Female',
                            bg='pink', variable=female, onvalue=1, offvalue=0)
    femaleOpt.grid(row=3, column=1, pady=0, padx=30, sticky=W)

    submitBtn = Button(frame2, text="Play PDF File", command=speak_text,
                       activeforeground='green', padx=60, pady=10, fg='white', bg='black', font="Arial 12")
    submitBtn.grid(row=4, column=0, pady=65)

    stopBtn = Button(frame2, text='Stop Playing', command=stop_speaking,
                     activeforeground='green', padx=60, pady=10, fg='white', bg='black', font='Arial 12')
    stopBtn.grid(row=4, column=1, pady=65)

if __name__ == "__main__":
    mytext, rate, male, female = "", '100', 0, 0
    engine = pyttsx3.init(driverName='espeak')

    root = Tk()
    Application(root)
    root.mainloop()

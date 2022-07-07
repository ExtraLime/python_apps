import pyttsx3

eng = pyttsx3.init(driverName='espeak')
eng.setProperty('rate',200)
eng.setProperty('voice','m1')

eng.say('hello world')
eng.runAndWait()


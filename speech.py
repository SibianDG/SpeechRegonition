import time
import os
import speech_recognition as sr

DIR = './chunks'
numberOfItems = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
print("NumberOfFiles: ", numberOfItems)

fileName = 'Annelies Verbeke – Het kortverhaal doorgelicht'

r = sr.Recognizer()

for i in range(numberOfItems):
    print(i+17)
    file = './chunks/chunk' + str(i+17) + '.flac'
    audio_file = sr.AudioFile(file)
    with audio_file as source:
        audio_file = r.record(source)
        print("Starting convert from audio to text")
        try:
            text = r.recognize_google(audio_data=audio_file, language="nl-be")
        except:
            print("trying Eng")
            try :
                text = r.recognize_google(audio_data=audio_file, language="en-GB")
            except:
                print("Sorry couldn't make it work")
                text = "(some period wa not recognized)"

        text += " "

        print("Start writeting to ", fileName)
        file1 = open(fileName + ".txt", "a")
        file1.write(text)
        file1.close()
        print("End writeting")
        print("sleep")
        # time.sleep(30)

print("Done!")
print()
# print(text)

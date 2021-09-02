import time
import os
import speech_recognition as sr

DIR = './chunks'
numberOfItems = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
print("NumberOfFiles: ", numberOfItems)

fileName = 'A Tour of Lacan\'s Graph of Desire.flac'

r = sr.Recognizer()

for i in range(numberOfItems):
    print(i)
    file = './chunks/chunk' + str(i) + '.flac'
    audio_file = sr.AudioFile(file)
    with audio_file as source:
        audio_file = r.record(source)
        print(f"Starting to convert chunck {i} of {numberOfItems} to text")
        try:
            text = r.recognize_google(audio_data=audio_file, language="en-GB")
        except:
            print("trying Eng")
            try:
                text = r.recognize_google(audio_data=audio_file, language="en-US")
            except:
                print("a certain period was not recognized.")
                text = "(a certain period was not recognized.)"

        text += " "

        print("Start writing to ", fileName.replace("flac", "txt"))
        file1 = open(fileName[:-2] + ".txt", "a")
        file1.write(text)
        file1.close()
        print("End writing")

print("Done!")
print()

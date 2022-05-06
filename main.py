from pydub import AudioSegment
# from pydub.utils import mediainfo
from pydub.utils import make_chunks
import math
import os
import speech_recognition as sr
import re

file = ''
language1 = ''
language2 = ''
myaudio = ''


def start():
    global file, language1, language2

    notCorrect = True
    while notCorrect:
        file = input("Give the filename: ")
        try:
            print("Checking if the file is good.")
            #if file.endswith('.mp3'):
            #    print("mp3 file detected")
            #    audio = AudioSegment.from_mp3(file)
            #    file = file.replace('.mp3', '.flac')
            #    audio.export(file)
            AudioSegment.from_mp3(file)
            notCorrect = False
        except Exception as e:
            print(f"Bad file!\nError: {e}")

    print("Choose 2 languages that are spoken in the audio file:\n"
          "Examples: Dutch (Belgium) = nl-BE, Dutch (Netherlands) = nl-NL\n"
          "British English = en-GB, American English = en-US\n"
          "French = fr-FR.")
    regex = "[a-z]{2,3}-[A-Z]{2,4}"
    notCorrect = True
    while notCorrect:
        language1 = input("Give languages 1: ")
        if re.search(regex, language1) is None:
            print("Give a correct language")
        else:
            notCorrect = False

    language2 = input("Give languages 2: ")
    if re.search(regex, language2) is not None:
        language2 = ''


def to_chunks():
    global file, language1, language2, myaudio
    print(file, ' to chunks')
    myaudio = AudioSegment.from_mp3(file)
    channel_count = myaudio.channels  # Get channels
    sample_width = myaudio.sample_width  # Get sample width
    duration_in_sec = len(myaudio) / 1000  # Length of audio in sec
    sample_rate = myaudio.frame_rate

    print("sample_width=", sample_width)
    print("channel_count=", channel_count)
    print("duration_in_sec=", duration_in_sec)
    print("frame_rate=", sample_rate)
    bit_rate = 16  # assumption , you can extract from mediainfo("test.wav") dynamically

    wav_file_size = (sample_rate * bit_rate * channel_count * duration_in_sec) / 20
    print("wav_file_size = ", wav_file_size)

    file_split_size = 20000000  # 10Mb OR 10, 000, 000 bytes
    total_chunks = wav_file_size // file_split_size

    # Get chunk size by following method #There are more than one ofcourse
    # for  duration_in_sec (X) -->  wav_file_size (Y)
    # So   whats duration in sec  (K) --> for file size of 10Mb
    #  K = X * 10Mb / Y

    chunk_length_in_sec = math.ceil((duration_in_sec * 10000000) / wav_file_size)  # in sec
    chunk_length_ms = chunk_length_in_sec * 1000
    chunks = make_chunks(myaudio, chunk_length_ms)

    # Export all of the individual chunks as wav files

    if not os.path.exists('chunks'):
        os.makedirs('chunks')

    for i, chunk in enumerate(chunks):
        chunk_name = "chunks/chunk{0}.flac".format(i)
        print("exporting", chunk_name)
        chunk.export(chunk_name, format="flac")


def speech_to_text():
    global file, language1, language2

    DIR = './chunks'
    numberOfItems = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
    print("NumberOfFiles: ", numberOfItems)

    r = sr.Recognizer()

    for i in range(numberOfItems):
        print(i)
        chunkFile = './chunks/chunk' + str(i) + '.flac'
        audio_file = sr.AudioFile(chunkFile)
        with audio_file as source:
            audio_file = r.record(source)
            print(f"Starting to convert chunck {i} of {numberOfItems} to text")
            try:
                text = r.recognize_google(audio_data=audio_file, language=language1)
            except:
                if language2 != '':
                    print("trying 2nd languages")
                    try:
                        text = r.recognize_google(audio_data=audio_file, language=language2)
                    except:
                        print("a certain period was not recognized.")
                        text = "(a certain period was not recognized.)"

            text += " "

            print("Start writing to ", file.replace(".flac", ""), ".txt")
            file1 = open(file.replace(".flac", "") + ".txt", "a")
            file1.write(text)
            file1.close()
            print("End writing")

    print("Done!")
    print()


start()
to_chunks()
speech_to_text()

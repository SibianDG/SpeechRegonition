from pydub import AudioSegment
# from pydub.utils import mediainfo
from pydub.utils import make_chunks
import math

file = 'Annelies Verbeke – Het kortverhaal doorgelicht.flac'

myaudio = AudioSegment.from_file(file, "flac")
channel_count = myaudio.channels  # Get channels
sample_width = myaudio.sample_width  # Get sample width
duration_in_sec = len(myaudio) / 1000  # Length of audio in sec
sample_rate = myaudio.frame_rate

print("sample_width=", sample_width)
print("channel_count=", channel_count)
print("duration_in_sec=", duration_in_sec)
print("frame_rate=", sample_rate)
bit_rate = 16  # assumption , you can extract from mediainfo("test.wav") dynamically

wav_file_size = (sample_rate * bit_rate * channel_count * duration_in_sec) / 25
print("wav_file_size = ", wav_file_size)

file_split_size = 25000000  # 10Mb OR 10, 000, 000 bytes
total_chunks = wav_file_size // file_split_size

# Get chunk size by following method #There are more than one ofcourse
# for  duration_in_sec (X) -->  wav_file_size (Y)
# So   whats duration in sec  (K) --> for file size of 10Mb
#  K = X * 10Mb / Y

chunk_length_in_sec = math.ceil((duration_in_sec * 10000000) / wav_file_size)  # in sec
chunk_length_ms = chunk_length_in_sec * 1000
chunks = make_chunks(myaudio, chunk_length_ms)

# Export all of the individual chunks as wav files

for i, chunk in enumerate(chunks):
    chunk_name = "chunks/chunk{0}.flac".format(i)
    print("exporting", chunk_name)
    chunk.export(chunk_name, format="flac")

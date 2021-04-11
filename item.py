from tinytag import TinyTag

file = './chunks/chunk52.flac'

tag = TinyTag.get(file)

print(tag.duration)
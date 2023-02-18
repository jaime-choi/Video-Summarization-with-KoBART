import os

def convertTest(filePath: str, newFileName: str):
    com1 = f"ffmpeg -i {filePath} {newFileName}.mp3"
    com2 = f"ffmpeg -i {newFileName}.mp3 {newFileName}.wav"
    os.system(com1)
    os.system(com2)



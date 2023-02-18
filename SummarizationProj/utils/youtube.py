from pytube import YouTube
import xml.etree.ElementTree as ElementTree
from html import unescape
import os
import speech_recognition as sr
import uuid

def xml_to_str(xml_captions) -> str:
    segments = []
    root = ElementTree.fromstring(xml_captions)
    count_line = 0
    for child in list(root.findall('body/p')):
        text = "".join(child.itertext()).strip()
        if not text:
            continue
        count_line += 1
        caption = unescape(text.replace("\n", " ").replace("  ", " "), )
        segments.append(caption)
    return " ".join(segments).strip()

def getVidInfos(url):
    vid = YouTube(url)
    title = vid.title
    thumbnail = vid.thumbnail_url
    channel = vid.channel_id
    description = vid.description
    caption = vid.captions
    try:
        captions = caption.get_by_language_code("a.ko").xml_captions
        caption_text = xml_to_str(captions)
    except:
        caption_text = getVid(vid)
    return title, thumbnail, channel, description, caption_text

def getVid(vid: YouTube):
    audioVid = vid.streams.filter(only_audio=True).first()
    outfile = audioVid.download()
    new_name = str(uuid.uuid4())
    os.rename(outfile, new_name)
    r = sr.Recognizer()
    com1 = f"ffmpeg -i C:/Users/Main/학회/플젝/SummarizationProj/{new_name} {new_name}.mp3"
    com2 = f"ffmpeg -i {new_name}.mp3 {new_name}.wav"
    os.system(com1)
    os.system(com2)
    audio = sr.AudioFile(f"{new_name}.wav")
    with audio as source:
        audio = r.record(source)
    caption_text = r.recognize_google(audio_data=audio, language="ko-KR", show_all=True)
    return caption_text

# TEST
if __name__ == "__main__":
    print(getVid(YouTube("https://www.youtube.com/watch?v=6cCrkCcGngM")))
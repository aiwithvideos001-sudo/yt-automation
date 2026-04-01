import os, json, requests, urllib.request
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import random

topics = [
    "मेहनत कभी बेकार नहीं जाती, सफलता जरूर मिलती है।",
    "हर मुश्किल के बाद एक नई शुरुआत होती है।",
    "जो सपने देखते हैं वो ही सपने पूरे करते हैं।",
    "आज की मेहनत कल की सफलता बनती है।",
    "हार मत मानो, जीत तुम्हारी है।"
]
topic = random.choice(topics)

tts = gTTS(text=topic, lang='hi')
tts.save("voice.mp3")

urllib.request.urlretrieve("https://images.unsplash.com/photo-1502082553048-f009c37129b9?w=1280", "bg.jpg")

audio = AudioFileClip("voice.mp3")
ImageClip("bg.jpg").set_duration(audio.duration).set_audio(audio).write_videofile("video.mp4",fps=24)

yt = build('youtube','v3',credentials=Credentials(**json.loads(os.environ['YOUTUBE_CREDENTIALS'])))
yt.videos().insert(part="snippet,status",body={"snippet":{"title":topic[:80],"description":topic,"categoryId":"22"},"status":{"privacyStatus":"public"}},media_body=MediaFileUpload("video.mp4")).execute()
print("Done!")

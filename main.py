import os
import json
import requests
import google.generativeai as genai
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

GEMINI_KEY = os.environ['GEMINI_API_KEY']
PIXABAY_KEY = os.environ['PIXABAY_KEY']
YT_CREDS = json.loads(os.environ['YOUTUBE_CREDENTIALS'])

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')
topic = model.generate_content("Give me one interesting motivational fact in Hindi. Only the fact, nothing else.").text

tts = gTTS(text=topic, lang='hi')
tts.save("voice.mp3")

hits = requests.get(f"https://pixabay.com/api/?key={PIXABAY_KEY}&q=motivation&image_type=photo&per_page=3").json()['hits']
img_data = requests.get(hits[0]['largeImageURL']).content
with open("bg.jpg","wb") as f:
    f.write(img_data)

audio = AudioFileClip("voice.mp3")
clip = ImageClip("bg.jpg").set_duration(audio.duration).set_audio(audio)
clip.write_videofile("video.mp4", fps=24)

creds = Credentials(**YT_CREDS)
youtube = build('youtube','v3',credentials=creds)
youtube.videos().insert(
    part="snippet,status",
    body={"snippet":{"title":topic[:80],"description":topic,"categoryId":"22"},"status":{"privacyStatus":"public"}},
    media_body=MediaFileUpload("video.mp4")
).execute()
print("Uploaded!")

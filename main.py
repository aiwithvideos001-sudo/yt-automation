import os, json, requests
from gtts import gTTS
from google import genai
from moviepy.editor import ImageClip, AudioFileClip
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])
topic = client.models.generate_content(model='gemini-2.0-flash',contents='Give me one motivational fact in Hindi. Only the fact.').text

tts = gTTS(text=topic, lang='hi')
tts.save("voice.mp3")

hits = requests.get(f"https://pixabay.com/api/?key={os.environ['PIXABAY_KEY']}&q=motivation&image_type=photo&per_page=3").json()['hits']
with open("bg.jpg","wb") as f:
    f.write(requests.get(hits[0]['largeImageURL']).content)

audio = AudioFileClip("voice.mp3")
ImageClip("bg.jpg").set_duration(audio.duration).set_audio(audio).write_videofile("video.mp4",fps=24)

yt = build('youtube','v3',credentials=Credentials(**json.loads(os.environ['YOUTUBE_CREDENTIALS'])))
yt.videos().insert(part="snippet,status",body={"snippet":{"title":topic[:80],"description":topic,"categoryId":"22"},"status":{"privacyStatus":"public"}},media_body=MediaFileUpload("video.mp4")).execute()
print("Done!")

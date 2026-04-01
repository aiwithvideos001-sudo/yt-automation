import os, json, urllib.request, random
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

stories = [
    {"title": "एक भिखारी से Billionaire तक 🔥", "script": "क्या तुम जानते हो... एक इंसान ने सिर्फ एक decision से अपनी पूरी ज़िंदगी बदल दी? उसके पास कुछ नहीं था। कोई पैसा नहीं। कोई connection नहीं। लोग उसे देखकर हँसते थे। लेकिन उसने हार नहीं मानी। रोज़ उठता था। रोज़ काम करता था। और एक दिन... वही लोग जो हँसते थे... उसके दरवाज़े पर खड़े थे। तुम्हारी story अभी खत्म नहीं हुई। उठो। चलो। रुको मत।"},
    {"title": "जब पूरी दुनिया ने छोड़ दिया 💪", "script": "सोचो उस इंसान के बारे में... जिसे उसके सबसे करीबी लोगों ने भी छोड़ दिया। Family ने कहा तू fail है। दोस्तों ने कहा छोड़ दे यह सपना। लेकिन उस रात उसने एक वादा किया। मैं साबित करूँगा। सिर्फ खुद को। तुम्हारे पास भी वही hunger है। बस उसे जगाना है। आज नहीं जागे तो कब जागोगे?"},
    {"title": "यह 5 मिनट तुम्हारी ज़िंदगी बदल सकते हैं ⚡", "script": "मैं तुमसे एक सवाल पूछता हूँ। 5 साल बाद का तुम... आज के तुम्हें देखकर क्या सोचेगा? क्या वो proud होगा? ज़्यादातर लोग रोज़ उठते हैं। वही काम करते हैं। और साल बीत जाते हैं। लेकिन कुछ लोग एक decision लेते हैं। आज। अभी। मैं वो बनूँगा जो मैं बनना चाहता हूँ। तुम वो decision कब लोगे? आज। कल नहीं। आज।"},
    {"title": "अंधेरे के बाद रोशनी ज़रूर आती है 🌅", "script": "Thomas Edison ने 10,000 बार fail किया। हर बार लोगों ने कहा छोड़ दो। उसने कहा मैं fail नहीं हुआ। मैंने 10,000 तरीके ढूंढे जो काम नहीं करते। तुम्हारी failure तुम्हारी कमज़ोरी नहीं। तुम्हारी failure तुम्हारा data है। हर गिरावट तुम्हें एक कदम और ऊपर ले जाती है। तो उठो। एक बार और।"},
    {"title": "गरीबी से Empire तक 😢🔥", "script": "एक माँ थी। दो बच्चे थे। घर में खाना नहीं था। पति छोड़ कर चला गया। कोई job नहीं। लोगों ने कहा अब क्या करोगी? उसने कहा देखना। उसने रात को काम किया। कभी रोई तो अकेले में रोई। बच्चों के सामने हमेशा मुस्कुराई। तुम्हारी मजबूरी भी तुम्हारी ताकत है। जब रास्ता नहीं होता तभी असली रास्ता बनाया जाता है।"}
]

images = [
    "https://images.unsplash.com/photo-1502082553048-f009c37129b9?w=1280",
    "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1280",
    "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1280",
    "https://images.unsplash.com/photo-1470770841072-f978cf4d019e?w=1280",
    "https://images.unsplash.com/photo-1495107334309-fcf20504a5ab?w=1280"
]

story = random.choice(stories)
img_url = random.choice(images)

print(f"Making: {story['title']}")

tts = gTTS(text=story['script'], lang='hi', slow=True)
tts.save("voice.mp3")

urllib.request.urlretrieve(img_url, "bg.jpg")

audio = AudioFileClip("voice.mp3")
ImageClip("bg.jpg").set_duration(audio.duration).set_audio(audio).write_videofile("video.mp4", fps=24)

yt = build('youtube','v3',credentials=Credentials(**json.loads(os.environ['YOUTUBE_CREDENTIALS'])))
yt.videos().insert(
    part="snippet,status",
    body={"snippet":{"title":story['title'],"description":story['script']+"\n\n#motivation #hindi #success","categoryId":"22","tags":["motivation","hindi","success"]},"status":{"privacyStatus":"public"}},
    media_body=MediaFileUpload("video.mp4")
).execute()
print("Done!")

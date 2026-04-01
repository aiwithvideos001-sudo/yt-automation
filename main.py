import os, json, urllib.request, random
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

stories = [
    {
        "title": "Ek Garib Ladke Ki Kahani Jo Aaj Billionaire Hai",
        "script": """Imagine karo... ek 14 saal ka ladka, jiske ghar mein bijli nahi thi.
Raat ko wo candle ki roshni mein padhta tha.
Log kehte the - tu kuch nahi kar sakta.
Aaj us ladke ka naam hai Elon Musk.
Usne prove kiya - circumstances change ho sakti hain, agar will power ho.
Remember - your current situation is not your final destination.
Keep going. Keep pushing. Your time is coming."""
    },
    {
        "title": "99 Baar Fail Hone Ke Baad Bhi Nahi Mana",
        "script": """Ek aadmi tha jisne 99 baar fail hone ke baad bhi nahi maana.
Uski company bankrupt ho gayi. Uski wife chali gayi. Log hanste the usse.
Phir bhi wo uthta raha. Roz. Ek aur baar.
Aaj wo aadmi - Colonel Sanders - KFC ka founder hai.
65 saal ki umar mein usne apna pehla restaurant khola.
Moral - Kabhi mat socho ki tumhari umar ho gayi ya time nikal gaya.
Your story is still being written. Don't close the book yet."""
    },
    {
        "title": "Woh Raat Jo Sab Kuch Badal Deti Hai",
        "script": """Ek raat aisi hoti hai - har insaan ki zindagi mein.
Jab andhera itna gehra hota hai - ki lagta hai - sab khatam ho gaya.
Us raat - ek choice hoti hai.
Ya toot jaao. Ya toot ke bhi khade raho.
Jo log aaj successful hain - unhone woh raat choose ki - jab khade rehne ki himmat di.
Teri bhi aisi raat aayegi. Ya shayad abhi chal rahi hai.
Bas ek kaam karo - kal ki subah dekho.
Kyunki - after every dark night - there is a bright morning.
And that morning - is yours."""
    },
    {
        "title": "5 Saal Pehle Wala Tu Aur Aaj Ka Tu",
        "script": """Socho - 5 saal pehle - tum kahan the?
Kya tumne socha tha - aaj tum yahaan honge?
Nahi na?
Life aisi hi hoti hai - unexpected.
Tum sirf ek decision door ho - ek aisi zindagi se - jo tum actually chahte ho.
Woh decision kya hai - sirf tum jaante ho.
But ek baat yaad rakho -
5 saal baad - ek naya tum hoga.
Sawaal yeh hai - kya woh tum - aaj ke tumse khush hoga?
Start today. Not tomorrow. TODAY."""
    },
    {
        "title": "Jab Duniya Ne Muh Mod Liya",
        "script": """Jab Steve Jobs ko apni hi company Apple se nikala gaya -
Duniya ne kaha - ab iska career khatam.
Jab J.K. Rowling 12 publishers ne reject kiya -
Duniya ne kaha - yeh writer nahi ban sakti.
Jab Michael Jordan ko school basketball team se nikala gaya -
Duniya ne kaha - yeh sports mein nahi jayega.
Phir kya hua - yeh sab jante hain.
Toh jab duniya tujhe reject kare -
Yaad rakhna - rejection is God's protection.
Aur tujhe sirf ek haan chahiye. Sirf ek."""
    }
]

creds_data = json.loads(os.environ['YOUTUBE_CREDENTIALS'])
yt = build('youtube','v3',credentials=Credentials(**creds_data))

images = [
    "https://images.unsplash.com/photo-1502082553048-f009c37129b9?w=1280",
    "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1280",
    "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1280"
]

selected = random.sample(stories, 3)

for i, story in enumerate(selected):
    print(f"Making video {i+1}: {story['title']}")
    
    tts = gTTS(text=story['script'], lang='hi', slow=False)
    tts.save(f"voice_{i}.mp3")
    
    img_url = images[i % len(images)]
    urllib.request.urlretrieve(img_url, f"bg_{i}.jpg")
    
    audio = AudioFileClip(f"voice_{i}.mp3")
    clip = ImageClip(f"bg_{i}.jpg").set_duration(audio.duration).set_audio(audio)
    clip.write_videofile(f"video_{i}.mp4", fps=24)
    
    yt.videos().insert(
        part="snippet,status",
        body={
            "snippet":{
                "title": story['title'],
                "description": story['script'] + "\n\n#motivation #success #hindi #inspiration",
                "categoryId": "22",
                "tags": ["motivation","success","hindi motivation","inspiration","life"]
            },
            "status":{"privacyStatus":"public"}
        },
        media_body=MediaFileUpload(f"video_{i}.mp4")
    ).execute()
    print(f"Video {i+1} uploaded!")

print("All 3 videos done!")

# line of action:
# 1. get the search string from the user
# 2. search it in youtube, get the first result's id, (esVRiC6s9f8)
# 3. ytdl will get us the video or the audio.
# 4. aac, convert to mp3, change ID3 tags

import sys
from urllib import request
from urllib import parse
from bs4 import BeautifulSoup

import urllib.request

import requests

arguments = sys.argv
search_term = arguments[1]

# https://www.youtube.com/results?search_query=ducati+monster+821+top+speed

url = "https://www.youtube.com/results?search_query=" + parse.quote(search_term)

# response = requests.get("https://www.youtube.com/results?search_query=ducati+monster+821+top+speed")
response = urllib.request.urlopen(url).read()
html = str(response, 'utf-8')

pos = html.find('watch?v=')
pos += 8
key = html[pos:pos + 30]

posQ = key.find('"')
youtubeId = key[0: posQ]

# exercise 1:
# pos = html.find('watch?v=') .
# specify that v= is the start and " is the end.
# get the substring

print('The youtube id is ' + str(youtubeId))

import youtube_dl

options = {
    'format': 'bestvideo/best',
    # 'postprocessors': [{
    #     'key': 'FFmpegExtractAudio',
    # 'preferredcodec': 'mp3',
    # 'preferredquality': '192',
    # }],
}

yt = youtube_dl.YoutubeDL(options)
yt.download(['https://www.youtube.com/watch?v=' + str(youtubeId)])

print('The file is now downloaded')


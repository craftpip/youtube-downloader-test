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


def search_youtube(term):
    url = "https://www.youtube.com/results?search_query=" + parse.quote(search_term)
    response = requests.get("https://www.youtube.com/results?search_query=ducati+monster+821+top+speed", headers={
        'user-agent': 'Opera/9.80 (iPhone; Opera Mini/8.0.0/34.2336; U; en) Presto/2.8.119 Version/11.10'
    })

    # todo: get the json data, and get the complete video list,
    # get out the video seconds, description, channel name, title, and video id, payment required flag
    # for 2020-08-26
    html = str(response.content, 'utf-8')

    # find and get video id from html string.
    pos = html.find('watch?v=')
    pos += 8
    key = html[pos:pos + 30]

    posQ = key.find('"')
    youtubeId = key[0: posQ]

    return youtubeId


# https://www.youtube.com/results?search_query=ducati+monster+821+top+speed

def download_youtube(youtubeId):
    # exercise 1:
    # pos = html.find('watch?v=') .
    # specify that v= is the start and " is the end.
    # get the substring
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


def init_function():
    print('Searching for ' + str(search_term))
    youtubeId = search_youtube(search_term)
    print('Found first result on youtube, id is ' + str(youtubeId))
    download_youtube(youtubeId)
    print('The file is now downloaded')


init_function()

# line of action:
# 1. get the search string from the user
# 2. search it in youtube, get the first result's id, (esVRiC6s9f8)
# 3. ytdl will get us the video or the audio. mp3
# 4. aac, convert to mp3, change ID3 tags. thumbnail

# 5. setup selenium to read whatsapp web
#       read music and memes group, find messages containing spotify links
#       read the link get the title, download the video, upload to server, and share the link.


import json
import sys
from time import sleep
from urllib import request
from urllib import parse
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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


def search_youtube2(term):
    url = "https://www.youtube.com/results?search_query=" + parse.quote(search_term)
    response = requests.get(url, headers={
        # 'user-agent': 'Opera/9.80 (iPhone; Opera Mini/8.0.0/34.2336; U; en) Presto/2.8.119 Version/11.10'
    })

    # todo: get the json data, and get the complete video list,
    # get out the video seconds, description, channel name, title, and video id, payment required flag
    # for 2020-08-26
    html = str(response.content, 'utf-8')

    # find and get video id from html string.

    start_string = 'window["ytInitialData"] = '
    end_string = 'window["ytInitialPlayerResponse"]'

    start_position = html.find(start_string)
    start_position += len(start_string)

    end_position = html.find(end_string)

    # get the youtube object
    object_string = html[start_position: end_position]

    # trim the end and remove the last ; semi colon
    my_fav_object = object_string.strip()[0:-1]

    fav_object = json.loads(my_fav_object)

    list = fav_object['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']

    largest_seconds = 0
    selected_video = False

    for item in list:
        if 'videoRenderer' in item:
            videoId = item['videoRenderer']['videoId']
            title = item['videoRenderer']['title']['runs'][0]['text']
            time = item['videoRenderer']['lengthText']['simpleText']
            description = item['videoRenderer']['descriptionSnippet']['runs'][0]['text']
            channel_name = item['videoRenderer']['ownerText']['runs'][0]['text']
            this_video_seconds = give_me_seconds(time)
            if this_video_seconds > largest_seconds:
                largest_seconds = this_video_seconds
                selected_video = {
                    'video_id': videoId,
                    'title': title,
                    'time': this_video_seconds,
                    'description': description,
                    'channel_name': channel_name
                }

    if selected_video == False:
        print('Could not find anything')
        return False
    else:
        print('The longest video we found was ' + str(selected_video['time']) + ' with title ' + str(selected_video['title']))

    return selected_video


def give_me_seconds(time):
    time_array = time.split(':')
    time_array.reverse()
    # time_array.
    c = len(time_array) - 1
    seconds = 0
    while c >= 0:
        sec = int(time_array[c])
        c2 = c
        while (c2):
            sec *= 60
            c2 -= 1
        seconds += sec
        c -= 1

    return seconds


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


def loop():
    sleep(2)
    loop()


def init_function():
    driver = webdriver.Chrome(executable_path=r'D:\xampp7.3\htdocs\youtube-downloader-test\chromedriver.exe')
    driver.get("http://www.python.org")

    print('Searching for ' + str(search_term))
    video = search_youtube2(search_term)
    print('Found first result on youtube, id is ' + str(video['title']))
    download_youtube(video['video_id'])
    print('The file is now downloaded')


init_function()

from twitch import TwitchClient
import os
import sys
import requests
import urllib.request
import argparse
import json
import re
from moviepy.editor import VideoFileClip, concatenate_videoclips
from math import floor

client = TwitchClient(client_id="----your-client-id-here-----", oauth_token="----your-oauth-token-here------")

# Update Video Description

def get_description():
    with open("clips.json") as f:
        data = json.load(f)

    with open("desc.txt","w",encoding="utf-8") as myfile:
        myfile.write("Streamers in this video are : \n\n")
        tm = 5
        for i,clip in enumerate(data):
            name = data[clip]["display_name"]
            title = data[clip]["title"]
            mm = str(int(tm/60))
            ss = str(int(tm)%60)
            if(int(tm)%60 < 10):
                ss = '0'+ss
            myfile.write(f"Clip #{i+1} : [{mm}:{ss}] : {title}\n")
            tm += data[clip]["duration"]
            myfile.write( f" ➠ https://twitch.tv/{name}\n\n")

#Render Video clips from Downloaded Clips

def get_clip_files(path: str):
    clips = []

    for file in os.listdir(path):
        if file.endswith(".mp4"):
            clips.append(os.path.join(path, file))
    return clips


def render():
    path = "clips/"
    print(f"Going to render video in {path}\n")

    videos = []

    for video in get_clip_files(path):

        movie = VideoFileClip(video, target_resolution=(720, 1280))
        name = video.replace(path, "") \
            .replace("_", " ") \
            .replace("\\", "")

        videos.append(movie)

        print(f"Added {name} to be rendered")

        del video
        del movie
        del name

    final = concatenate_videoclips(videos, method="compose")
    final.write_videofile(f"{path}/rendered.mp4", fps=30)

    print()
    print("Video is done rendering!\n")

# Get and Download clips from Twitch

def get_clip_data(slug: str):
    clip_info = client.clips.get_by_slug(slug)
    thumb_url = clip_info['thumbnails']['medium']
    title = clip_info['title']
    print(title)
    slice_point = thumb_url.index("-preview-")
    mp4_url = thumb_url[:slice_point] + '.mp4'
    return mp4_url, title


def get_slug(clip: str):
    slug = clip.split('/')
    return slug[len(slug) - 1]

def get_clips(length: int):
    length *= 60
    data = {}

    response = client.clips.get_top(  channel = "ViditChess", game = "Chess", limit = 100 , period = "all")

    for clip in response:
        data[clip["tracking_id"]] = {
            "url": "https://clips.twitch.tv/" + clip["slug"],
            "title": clip["title"],
            "display_name": clip["broadcaster"]["display_name"],
            "duration": clip["duration"]
            }

    with open("clips.json", "w") as f:
        json.dump(data, f, indent=4)

    return data

def download_clip(clip: str):
    basepath = 'clips/'
    slug = get_slug(clip)
    mp4_url,thumb_url = get_clip_data(slug)
    out_filename = slug + ".mp4"
    output_path = (basepath + out_filename)


    # create the basepath directory
    if not os.path.exists(basepath):
        os.makedirs(basepath)


    try:
        urllib.request.urlretrieve(mp4_url, output_path, reporthook=dl_progress)
    except:
        print("An exception occurred")

    print("\n Video Downloaded")


def download_clips(data: dict , length: int):
    length *= 60
    names = []

    for clip in data:
        
        #print(clip)
        #print(clip['url'])
        download_clip(data[clip]['url'])
        length -= data[clip]["duration"]

        name = data[clip]["display_name"]

        if name not in names:
            names.append(name)
        
        print(f"Remaining video length: {floor(length)} seconds\n")

        if length <= 0:
            print("Downloaded all clips.\n")
            return names
        else:
            continue

def dl_progress(count, block_size, total_size):
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%" % percent)
    sys.stdout.flush()



# Get JSON clip data via Twitch API
data = get_clips( "--required-video-length--" )

# Download Clips
download_clips(data, "--required-video-length--" )  

# Render Clips
render()

# Update Description
get_description()

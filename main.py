#!/usr/local/bin/python3

import requests
import ffmpeg
import json
import datetime
import os
import music_tag
import argparse
from pathlib import Path

argParser = argparse.ArgumentParser()
argParser.add_argument("-f","--file",help="File name")
args = vars(argParser.parse_args())

def transcode(filename,nfilename):
    ffmpeg.input(filename).output(nfilename,map_metadata=-1,ar=44100,ac=2,**{'b:a':'192k'}).run()

def tag_file(filename,fields):
    audio = music_tag.load_file(filename)

    audio["tracktitle"] = fields["title"]
    audio["artist"] = fields["artist"]
    audio["album"] = fields["album"]
    audio["year"] = fields["year"]
    audio["albumartist"] = fields["artist"]
    audio["tracknumber"] = fields["tracknumber"]
    audio["discnumber"] = fields["discnumber"]
    audio["comment"] = fields["link"]

    audio.save()

token = os.getenv("TOKEN")
baseurl = "https://api.audd.io/"
ofolder = 'output'
filename = 'input/' + args['file']

ffmpeg.input(filename,ss=30,t=20).output('clip.flac').overwrite_output().run()

data = {
    'api_token': token,
    'return' : 'spotify'
}
files = {
    'file': open('clip.flac', 'rb'),
}
result = requests.post('https://api.audd.io/', data=data, files=files)
output = result.text
# print(output)

os.remove("clip.flac")

if json.loads(output)["result"] is not None :
    result = json.loads(output)["result"]
    fields = {
        "title" : result["spotify"]["name"],
        "artist" : result["artist"],
        "album" : result["spotify"]["album"]["name"],
        "date" : result["release_date"],
        "year" : datetime.datetime.strptime(result["release_date"],'%Y-%m-%d').strftime("%Y"),
        "tracknumber" : result["spotify"]["track_number"],
        "discnumber" : result["spotify"]["disc_number"],
        "label" : result["label"],
        "link" : result["song_link"]
    }

    base = Path(filename)
    npath = ofolder + "/" + fields["artist"] + "/" + fields["album"]
    os.system('mkdir -p "'+ npath + '"')

    if filename.lower().endswith(('.flac','.m4a','.mp3','.ogg')) :
        nfilename = npath + "/" + str(fields["tracknumber"]).zfill(2) + " - " + fields["title"] + base.suffix
        base.rename(nfilename)
    else :
        nfilename = npath + "/" + str(fields["tracknumber"]).zfill(2) + " - " + fields["title"] + ".mp3"
        transcode(filename,nfilename)

    tag_file(nfilename,fields)
else:
    print("No match")

from __future__ import unicode_literals
import urllib
import requests
import youtube_dl
import sys
import os
import json

def dowloadSong(videoID):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(id)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([videoID])


def downloadPlaylist(json_data, num_songs):
    print("Downloading Files...")
    download_count = 0
    for video in json_data['items']:
        # Track Progress
        download_count += 1

        # Grab the ID
        videoID = video['contentDetails']['videoId']

        if os.path.isfile(videoID + ".wav"):
            print(videoID + ".wav already found - Skipping...")
        else:
            try:
                # Download the song
                dowloadSong(videoID)

                print("Downloaded " + str(download_count) + " / " + str(num_songs))
            except youtube_dl.utils.RegexNotFoundError:
                print("The youtube-dl library is outdated... Quitting script")
                exit()
            except:
                print("Failed to download song: " + str(videoID))


api_root = 'https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults='
api_key = 'AIzaSyBUT4JOwUpvKAr20O2n0NRXncsqpPFhJRg'
DIR_PREFIX = 'songs/'


# Load config from JSON file
with open('config.json') as f:
    config = json.load(f)


# Make sure directories are in order
os.getcwd()

if not os.path.isdir(DIR_PREFIX):
    print("Creating Directory: " + DIR_PREFIX)
    os.mkdir(DIR_PREFIX)

# Change to output directory
os.chdir(DIR_PREFIX)


default_count = config['default_count']

for playlist in config['items']:
    # read some stuff from the JSON data
    playlist_id = playlist['playlist_id']
    genre = playlist['genre']
    num_songs = playlist['num']

    # Check for default
    if num_songs < 0:
        num_songs = default_count

    # Construct API call
    url = api_root + str(num_songs) + '&playlistId=' + playlist_id + '&key=' + api_key

    # Read from the API response
    json_data = requests.get(url).json()

    # Prepare to download
    if not os.path.isdir(genre):
        os.mkdir(genre)

    os.chdir(genre)

    print("Beginning dowload of playlist: " +  playlist_id + " [" + genre + "]\n")

    # Download each item from the playlist
    downloadPlaylist(json_data, num_songs)

    print("\n----------------------------------------------------------------------------------------------")
    print("Download Complete for playlist: " + playlist_id + " [" + genre + "]")
    print("----------------------------------------------------------------------------------------------\n")

    os.chdir("..")

print("\nFinished downloading all playlists")





# # Read the stuff from the arguments
# if len(sys.argv) < 3:
#     print("Usage: python " + __file__ + " playlist_id genre_name [num_songs]")
#     exit()
#
#
# playlist_id = sys.argv[1]
# genre = sys.argv[2]
#
# num_songs = 50
#
# if len(sys.argv) > 3:
#     num_songs = int(sys.argv[3])
#
#
# DIR_PREFIX = 'songs/'
#
# # Start things out :)
# os.getcwd()
#
# if not os.path.isdir(DIR_PREFIX):
#     os.mkdir(DIR_PREFIX)
#
# # change that sucka
# os.chdir(DIR_PREFIX)
#
# # Create directory if not exists
# if not os.path.isdir(genre):
#     os.mkdir(genre)
#
# os.chdir(genre)
#
#
# api_root = 'https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults='
# api_key = 'AIzaSyBUT4JOwUpvKAr20O2n0NRXncsqpPFhJRg'
#
# url = api_root + str(num_songs) + '&playlistId=' + playlist_id + '&key=' + api_key
#
# # Let's actually grab the stuff
# json_data = requests.get(url).json()
#
#
# print("Downloading Files...")
# download_count = 0
#
# # Print out each video ID
# for video in json_data['items']:
#     # Track Progress
#     download_count += 1
#
#     # Grab the ID
#     videoID = video['contentDetails']['videoId']
#
#     try:
#         # Download the song
#         dowloadSong(videoID)
#
#         print("Downloaded " + str(download_count) + " / " + str(num_songs))
#     except:
#         print("Failed to download song: " + str(videoID))
#
# print("----------------------------------------------------------------------------------------------")
# print("\n\nDownload Complete for genre [" + genre + "]. Playlist: " + playlist_id)
# print("----------------------------------------------------------------------------------------------")

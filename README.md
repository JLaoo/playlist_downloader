# Computer to Android Device YouTube Playlist Downloader

## Instructions

1) pip install -r requirements.txt
2) Edit CONFIG file (or not, you can also enter arguments directly into the terminal). PLAYLIST_URL takes in a YouTube playlist URL and PHONE_PATH takes in a path to a folder in your phone.
3) Enable developer mode and USB transfering on your phone.
4) Connect phone to computer.
4) python3 script.py

## Features

- End-to-end pipeline from YouTube playlist to downloaded playlist on your Android device.
- Automatically detects what current songs are in your phone to avoid extraneous downloads and duplicate songs.

## Notes

- Tested with a 2018 MacBook Pro and a Samsung Galaxy s9+.
- This script most probably will need some small tweaks to the code to work on another device. This code definitely does not work on Windows at all lol. 
- The current platform-tools is for Mac. You can download one for your OS [here](https://developer.android.com/studio/releases/platform-tools).
- You can find out how to enable developer mode [here](https://developer.android.com/studio/command-line/adb#Enabling).
- You can figure out folder paths and stuff by entering the adb shell and ls'ing and cd'ing around.

import os
from pytube import Playlist, YouTube
from moviepy.editor import *
import subprocess
from subprocess import PIPE
import requests
import shutil

def goodURL(url):
	return "www.youtube.com/playlist" in url and requests.get(url).status_code == 200

def executeShellCmd(cmd):
	p = subprocess.Popen(["platform-tools/adb","shell"],stdin=PIPE,stdout=PIPE, stderr=PIPE)
	result = p.communicate(cmd.encode())
	return result

if __name__ == "__main__":
	# Configure phone path and playlist url
	playlist_url = None
	phone_path = None
	try:
		f = open("CONFIG", "r")
		playlist_url_input = f.readline()
		phone_path_input = f.readline()
		f.close()
		playlist_url = playlist_url_input.split("PLAYLIST_URL:")[1]
		playlist_url = playlist_url.strip(" ")
		phone_path = phone_path_input.split("PHONE_PATH:")[1]
		if phone_path.startswith(" "):
			phone_path = phone_path[1:]
	except:
		print("Empty or incorrectly formatted CONFIG file! Empty CONFIG file has been recreated.")
		with open('CONFIG', 'w') as f:
			f.write('PLAYLIST_URL:\nPHONE_PATH:')
	if not goodURL(playlist_url) or playlist_url == None:
		if playlist_url != None:
			print("Invalid URL in CONFIG file!")
		while True:
			playlist_url = input("Please enter a YouTube playlist URL: ")
			if goodURL(playlist_url):
				break
			print("Invalid URL, please try again...")
	if phone_path == None:
		print("Failed to retrieve phone path due to empty or improperly formatted CONFIG file.")
		phone_path = input("Please enter the path to your playlist on your phone: ")
	result = executeShellCmd('ls ' + phone_path)
	while True:
		if result[1].decode() == '':
			break
		if 'no devices/emulators found' in result[1].decode():
			print("Please connect your phone and allow file access")
		elif 'No such file or directory' in result[1].decode():
			new_dir_ans = input("No such directory exists, would you like to create it? [y/n]")
			if new_dir_ans == "y":
				new_dir_out = executeShellCmd('mkdir ' + phone_path)
				if "Permission denied" in new_dir_out[1].decode():
					print("Unable to create directory, please try another path.")
				else:
					break
		else:
			break
		phone_path = input("Please enter the path to your playlist on your phone: ")
		result = executeShellCmd('ls ' + phone_path)
	# Download songs
	if not os.path.exists('temp'):
		os.makedirs('temp')
	else:
		shutil.rmtree('temp')
		os.makedirs('temp')
	local_playlist = result[0].decode().split('\n')
	local_playlist = set([s[:-4] for s in local_playlist if s.endswith('.mp3')])
	yt_playlist = {}
	playlist_obj = Playlist(playlist_url)
	for url in playlist_obj.video_urls:
		vid_obj = YouTube(url)
		vid_title = vid_obj.title
		while vid_title == "YouTube":
			vid_obj = YouTube(url)
			vid_title = vid_obj.title
		if vid_obj.title not in local_playlist:
			vid_obj.streams.get_lowest_resolution().download('temp/')
			base_path = 'temp/' + vid_obj.title
			video = VideoFileClip(base_path + '.mp4')
			video.audio.write_audiofile(base_path + '.mp3')
			subprocess.call("platform-tools/./adb push './{}' {}".format(base_path + '.mp3', phone_path), shell=True)
	shutil.rmtree('temp')








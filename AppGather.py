from pyechonest import config
config.ECHO_NEST_API_KEY='DNHLTV3RVDS7OAO58'

import json
import pyechonest

from pyechonest import track

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

from pyechonest import playlist
import time
from socket import *

import numpy as np
from sklearn.cluster import KMeans
from pyechonest import song

from scipy.spatial import distance
import os

from Tkinter import *
import tkMessageBox
import tkFileDialog

import thread

def beenClicked():
   if(button1["text"] == "Select a dataSet" or number2.get() == ""):
   	tkMessageBox.showinfo("Error!", "Fill out information!")
   else:
   	numberSong["state"] = 'disabled'
   	button1["state"] = 'disabled'
   	button2["state"] = 'disabled'
   	try:
   		thread.start_new_thread( gatherSongsThread, ("Thread-1", float(number2.get()), ) )
	except:
   		print "Error: unable to start thread"

def gatherSongsThread(threadName, delay):
	genres = []
	genres.append("classical")
	genres.append("pop")
	genres.append("rock")
	genres.append("rap")
	genres.append("punk")
   	genre_count = 0

	while 1:
		f = open(button1["text"], 'a')
		if(genre_count > len(genres) - 1):
			genre_count = 0
		songs = gatherSongs(genres[genre_count])
		print genres[genre_count]
		genre_count = genre_count + 1

		for song in songs:
			line = ""
			valid = True
			try:
				for x in range(0, len(song)):
					if(x != len(song) - 1):
						if ',' in str(song[x]):
							valid = False
						line = line + str(song[x]).encode(encoding='utf-8') + ","
					else:
						line = line + str(song[x]).encode(encoding='utf-8') 
				
				line = line + "\n"
			except UnicodeEncodeError:
				print "Unicode Error. Did not take this song"
				valid = False
			if valid:
				f.write(line.encode(encoding='utf-8'))
				print line
			
		f.close()
		time.sleep(delay)


def selectFile():
    # Select a File:
    root = Tk()
    root.withdraw()

    f = tkFileDialog.askopenfile(parent=root,mode='rb',title='Choose a file')
    if f != None:
    	button1.config(text=os.path.abspath(f.name))

   	f.close()

def gatherSongs( genre ):
	songs = []
	try:
		p = playlist.basic (type='genre-radio', artist_id=None, artist=None, song_id=None, song=None, track_id=None, dmca=False, results=1, buckets=None, limit=False, genres=genre)
		for v in p:
			data = []
			data.append(v.artist_id)
			data.append(v.artist_name)
			data.append(genre)
			data.append(v.audio_summary['danceability'])
			data.append(v.audio_summary['duration'])
			data.append(v.audio_summary['energy'])
			data.append(v.audio_summary['key'])
			data.append(v.audio_summary['liveness'])
			data.append(v.audio_summary['loudness'])
			data.append(v.audio_summary['mode'])
			data.append(v.audio_summary['speechiness'])
			data.append(v.audio_summary['tempo'])
			data.append(v.audio_summary['time_signature'])
			data.append(v.audio_summary['valence'])
			songs.append(data)
	except pyechonest.util.EchoNestAPIError:
		print "API ERROR"
	except:
		print "SOME ERROR"
	return songs


app = Tk()
app.title("Gather Dataset for Radiology")
app.geometry('450x180+200+200')

labelText3 = StringVar()
labelText3.set("Delay per API access call (in seconds):")
label3 = Label(app, textvariable=labelText3, height=4)
label3.pack()

number2 = StringVar(None)
numberSong = Entry(app, textvariable=number2)
numberSong.pack()

button1 = Button(app, text="Select a dataSet", width=18, command=selectFile)
button1.pack()

button2 = Button(app, text="Gather", width=10, command=beenClicked)
button2.pack()



app.mainloop()
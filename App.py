from pyechonest import config
config.ECHO_NEST_API_KEY='OFNIYW7MJ1OPFF9FH'

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
from operator import itemgetter
from Tkinter import *
import tkMessageBox
import tkFileDialog

features_names = []

features_names.append('danceability')
features_names.append('duration')
features_names.append('energy')
features_names.append('key')
features_names.append('liveness')
features_names.append('loudness')
features_names.append('mode')
features_names.append('speechiness')
features_names.append('tempo')
features_names.append('time_signature')
features_names.append('valence')

def beenClicked():
    features_clicked = []
    #To get data[] from them add 3.
    features_clicked.append(val1.get()) #Danceability, 1
    features_clicked.append(val2.get()) #Duration, 2
    features_clicked.append(val3.get()) #Energy, 3
    features_clicked.append(val4.get()) #Key, 4
    features_clicked.append(val5.get()) #Liveness, 5
    features_clicked.append(val6.get()) #Loudness, 6
    features_clicked.append(val7.get()) #Mode, 7
    features_clicked.append(val8.get()) #Speechiness, 8
    features_clicked.append(val9.get()) #Tempo, 9
    features_clicked.append(val10.get()) #Time_Signature, 10
    features_clicked.append(val11.get()) #Valence, 11
    #tkMessageBox.showinfo("Title", name.get() + str(features_clicked) )

    hasOneFeature = False
    for feature in features_clicked:
    	if feature:
    		hasOneFeature = True

    if button1.cget("text") == "" or name.get() == "" or numberInput.get() == "" or number2.get() == "" or hasOneFeature == False:
    	tkMessageBox.showinfo("Error!", "Fill out information!")
    else:
    	similar_artists = findSimilarArtists(button1.cget("text"), name.get(), int(number2.get()), float(numberInput.get()), features_clicked)
    	if len(similar_artists) == 0:
    		tkMessageBox.showinfo("Here are similar artists!", "There are no similar artists for your criteria!")
    	else:
    		limit_results = 5
    		results = ""
    		for i in range(0, len(similar_artists)):
    			if(i < limit_results):
	    			rating = "{0:.2f}".format(float(1 - float(similar_artists[i][1])/ float(numberInput.get())) * 100)
	    			results = results + similar_artists[i][0] + " (" + str(rating) + "%)"
	    			if(i != len(similar_artists) - 1):
	    				results = results + "\n"
    		tkMessageBox.showinfo("Here are similar artists!", results)	
    	

def selectFile():
    # Select a File:
    root = Tk()
    root.withdraw()

    f = tkFileDialog.askopenfile(parent=root,mode='rb',title='Choose a file')
    if f != None:
    	button1.config(text=os.path.abspath(f.name))

   	f.close()


def loadDataset(file, features_used):
	artist_id = []
	artist_name = []
	genre = []
	features = []
	f = open(file, "r")
	for line in f.readlines():
		process = line.split(",")
		#Take the first three cause we need it for later.
		artist_id.append(process[0])
		artist_name.append(process[1])
		genre.append(process[2])

		data = []
		for x in range(3, len(process)):
			if(process[x] != "None"):
				if(features_used[x - 3]):
					data.append(process[x])
			else:
				if(features_used[x - 3]):
					data.append(0)
		data = [float(i) for i in data]
		features.append(data)

	return artist_id, artist_name, genre, features

def findSimilarArtists( dataset, name_of_artist, how_many_of_their_songs, euclidean_threshold, features_used):
	#returning this, this contains INDEXES of similar artists. you must refer to artist_id, artist_name, genre array, etc for it to work.
	similar_artists = []
	#rebuild the data to select our features
	artist_id, artist_name, genre, features = loadDataset(dataset, features_used)
	k_means_cluster = KMeans(n_init = 5, random_state = 1)
	k_means_cluster.fit(features, genre)

	#get a single song
	songs_by_artist = song.search(artist=name_of_artist.lower(), results=how_many_of_their_songs, buckets=['audio_summary'])

	features_of_artist = []
	for i in range(0, len(songs_by_artist)):
		single_feature_set = []
		for g in range(0, len(features_used)):
			if features_used[g]:
				single_feature_set.append(songs_by_artist[i].audio_summary[features_names[g]])

		features_of_artist.append(single_feature_set)

	for x in range(0, len(features_of_artist)):
		clusters_belong = k_means_cluster.predict(features_of_artist[x])
		for i in range(0, len(clusters_belong)):
			for g in range(0, len(np.where(k_means_cluster.labels_ == clusters_belong[i])[0])):
				index = np.where(k_means_cluster.labels_ == clusters_belong[i])[0][g]
				euc_dist = distance.euclidean(features_of_artist[x], features[index])
				if euc_dist <= euclidean_threshold:
					if(artist_name[index].lower() != name_of_artist.lower()):
						if artist_name[index] not in [row[0] for row in similar_artists]:
							artist_data = []
							artist_data.append(artist_name[np.where(k_means_cluster.labels_ == clusters_belong[i])[0][g]])
							artist_data.append(euc_dist)
							similar_artists.append(artist_data)
	#sort the array based on second column.
	similar_artists = sorted(similar_artists, key=itemgetter(1))
	return similar_artists


    
app = Tk()
app.title("Radiology V1.0")
app.geometry('450x650+200+200')

labelText1 = StringVar()
labelText1.set("Please Enter an artist:")
label1 = Label(app, textvariable=labelText1, height=4)
label1.pack()

custName = StringVar(None)
name = Entry(app, textvariable=custName)
name.pack()

val1 = IntVar()
checkBox1 = Checkbutton(app, variable=val1, text="Danceability")
checkBox1.pack()

val2 = IntVar()
checkBox2 = Checkbutton(app, variable=val2, text="Duration")
checkBox2.pack()

val3 = IntVar()
checkBox3 = Checkbutton(app, variable=val3, text="Energy")
checkBox3.pack()

val4 = IntVar()
checkBox4 = Checkbutton(app, variable=val4, text="Key")
checkBox4.pack()

val5 = IntVar()
checkBox5 = Checkbutton(app, variable=val5, text="Liveness")
checkBox5.pack()

val6 = IntVar()
checkBox6 = Checkbutton(app, variable=val6, text="Loudness")
checkBox6.pack()

val7 = IntVar()
checkBox7 = Checkbutton(app, variable=val7, text="Mode")
checkBox7.pack()

val8 = IntVar()
checkBox8 = Checkbutton(app, variable=val8, text="Speechiness")
checkBox8.pack()

val9 = IntVar()
checkBox9 = Checkbutton(app, variable=val9, text="Tempo")
checkBox9.pack()

val10 = IntVar()
checkBox10 = Checkbutton(app, variable=val10, text="Time_Signature")
checkBox10.pack()

val11 = IntVar()
checkBox11 = Checkbutton(app, variable=val11, text="Valence")
checkBox11.pack()

labelText2 = StringVar()
labelText2.set("Euclidean distance:")
label2 = Label(app, textvariable=labelText2, height=4)
label2.pack()

number = StringVar(None)
numberInput = Entry(app, textvariable=number)
numberInput.pack()

labelText3 = StringVar()
labelText3.set("Number of songs:")
label3 = Label(app, textvariable=labelText3, height=4)
label3.pack()

number2 = StringVar(None)
numberSong = Entry(app, textvariable=number2)
numberSong.pack()

button1 = Button(app, text="Select a dataSet", width=18, command=selectFile)
button1.pack()

button2 = Button(app, text="Search", width=10, command=beenClicked)
button2.pack()



app.mainloop()
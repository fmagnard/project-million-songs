#!/usr/bin/python
# coding: utf-8

from urllib2 import Request, urlopen
import json
import time
import fileinput
import spotipy
import sys

def call_artist(name):
	try:
		results = spotify.search(q='artist:' + name, type='artist')
	except ValueError:
		time.sleep(1)
		results=call_artist(name)
	return results

def call_album(artist):
	try:
		results = spotify.artist_albums(artist['uri'], album_type='album')
	except ValueError:
		time.sleep(1)
		results=call_album(artist['uri'])
	return results


def call_search(id1):
	try:
		url1 = "https://api.spotify.com/v1/albums/%s" % id1
		request = Request(url1, headers=headers)
		response_body = urlopen(request).read()
		response_body = json.loads(response_body)
		results = response_body["release_date"]
	except ValueError:
		time.sleep(1)
		results = call_search(id1)
	return results



f_old= open("../ConvertToCSV/Output/features.tsv", "r")
f_new= open("Output/features.tsv","a+")
headers = {'Accept': 'application/json'}


count=0
for line in f_new:
	count=count+1

numero_line=0
f_new.write("\n")

spotify = spotipy.Spotify()
for line in f_old :
	numero_line=numero_line+1
	if (numero_line<count+1):
		element = line.split('\t')
	else:
		element = line.split('\t')
	
		if len(sys.argv) > 1:
			name = ' '.join(sys.argv[1:])
			alb = ' '.join(sys.argv[1:])
		else:
			name = element[9] #print(name)
			name = name[2:-1]
			alb = element[21]
			alb = alb[2:-1]
			#print(alb)

		results = call_artist(name)
		items = results['artists']['items']
		if len(items) > 0:
			artist = items[0]
			#print artist['name'], artist['uri']

		results = call_album(artist)
		albums = results['items']
		id1 = 0
		while results['next']:
			results = spotify.next(results)
			albums.extend(results['items'])

		for album in albums:
			if album['name']==alb:
				id1 = album['uri']

		print(id1)
		if id1==0:
			f_new.write(element[0]+"\t"+element[9]+"\t"+element[21]+"\t"+element[32])
		else:
			id1=id1[14:]
			#print(id1)
			results=call_search(id1)
			f_new.write(element[0]+"\t"+element[9]+"\t"+element[21]+"\t"+str(results)+"\n")

f_new.close()
f_old.close()
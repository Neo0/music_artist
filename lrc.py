import re
import urllib
import urlparse
from bs4 import BeautifulSoup
import csv
import os
import numpy as np
import pandas as pd

database = {}

url = u'http://www.lrcgc.com/'
def find_singers():
    singers_list = [] 
    response = urllib.urlopen('http://www.lrcgc.com/artist-00.html')
    data = response.read()
    soup = BeautifulSoup(data)    
    links = soup.findAll('a', href = re.compile(r'songlist.*.html'))
    for link in links:
        s = link.text
        l = link['href']
        singers_list.append([s, l])
    return singers_list

def find_songs(singer):
    singer_name, urls_0 = singer[0], singer[1]
    songs_href = [] 
    songs_list = [urls_0]
    song_list_old = [] 

    while len(songs_list) >0: 
        url_i = songs_list.pop() 
        song_list_old.append(url_i)
        response = urllib.urlopen(url+url_i)
        data = response.read()
        soup = BeautifulSoup(data)
        songs_list_links = soup.findAll('a', href = re.compile(r'songlist.*.html'))
        for link in songs_list_links:
            if link['href'] not in song_list_old:
                if link['href'] not in songs_list:
                    songs_list.append(link['href'])

        songs_href_list = soup.findAll('a', href = re.compile(r'lyric-.*.html'))
        for link in songs_href_list:
            songs_href.append(link['href'])

    return list(set(songs_href))

singers_list = find_singers()
database_singer = {}
try:
    for i in singers_list:
        database_singer[i[0].encode('utf-8')] = {"url": i[1].encode('utf-8')}
except:
    print "error!"
try:
    mi = pd.DataFrame(database_singer)
    print mi
    mi.to_csv("singer_info.csv")
    print len(database_singer)
except:
    print "singer_info.csv error!"
dic = {}
for singer in singers_list:
    try:
        ss = find_songs(singer)
        print singer[0].encode('utf-8') + '\t' + str(len(ss))
        dic[singer[0]] = ss
    except:
        continue


def parse_song_href(singer, song_url):
    complete_url = url + song_url
    response = urllib.urlopen(complete_url)
    data = response.read()
    soup = BeautifulSoup(data)
    name = soup.findAll('a', id = 'J_downlrc')[0]['href']
    download_url = url + name

    try:
        content = urllib.urlopen(download_url.encode('utf-8')).read() 
        with open('./' +  name.encode('utf-8').split('/')[1], 'w') as f:
            f.write(content)
        database[name.encode('utf-8').split('/')[1]] = {"url": download_url.encode('utf-8')}
        return download_url
    except:
        return False


for singer_name in dic.keys():
    for song_url in dic[singer_name]:
        print parse_song_href(singer_name, song_url)


mid = pd.DataFrame(database)
print mid
mid.to_csv("info.csv")
print len(database)
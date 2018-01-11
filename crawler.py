import requests
from bs4 import BeautifulSoup
import urllib
import os

url = "https://freemidi.org/"

target = {
    "https://freemidi.org/genre-pop",
    "https://freemidi.org/genre-rock",
    "https://freemidi.org/genre-classical",
    "https://freemidi.org/genre-country",
    "https://freemidi.org/genre-folk",
    "https://freemidi.org/genre-jazz",
    "https://freemidi.org/nationalanthems",
    "https://freemidi.org/movies",
    "https://freemidi.org/videogames"
}

cnt = 0

for uri in target:
    cat = uri.lstrip("https://freemidi.org/")
    result = requests.get(uri)
    c = result.content

    soup = BeautifulSoup(c)
    samples = soup.find_all("div",class_="genre-link-text")
    href_list = []

    for s in samples:
        a = s.a
        href_list.append(a["href"])

    music_list = []

    for href in href_list:
        result = requests.get(url+href)
        c = result.content
        soup = BeautifulSoup(c)
        for div in soup.find_all("div",class_="artist-song-cell"):
            music = {"url":div.find("a", {"itemprop": "url"})["href"],"name":div.find("a", {"itemprop": "url"}).text.strip().replace(" ","_")}
            music_list.append(music)
            try:
                print "get!" + music["name"]
            except UnicodeEncodeError:
                print "error!" + music["name"]

    for music in music_list:
        music_href = music["url"]
        tmp_list = music_href.split("-")
        download_url = url + "getter-"+ tmp_list[1]
        if not os.path.exists("output/"+cat):
            os.makedirs("output/"+cat)
        try:
            urllib.urlretrieve(download_url, "output/"+cat+"/"+music["name"]+".midi")
        except UnicodeEncodeError:
            print "error!" + music["name"]
        print "done!" + music["name"]
        cnt += 1
        print "cnt = " + str(cnt)

print "all = " + str(cnt)
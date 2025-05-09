import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import yt_dlp
import subprocess
import os


class SpotifyPlaylist:
    def __init__(self):
        pass


class Spotify:
    CREDS_FILE = "spotify_credentials.json"

    class Artist:
        def __init__(self, json):
            self.name = json["name"]

    class Track:
        def __init__(self, json):
            self.name = json["name"]
            self.track_number = json["track_number"]
            self.artists = []

            for a in json["artists"]:
                self.artists.append(Spotify.Artist(a))

        def print(self):
            print(self.name, "-", self.artists[0].name)

        def get_search_string(self) -> str:
            str = self.name

            if (len(self.artists) > 0):
                str += " - "
                str += self.artists[0].name

                for artist in self.artists[1:]:
                    str += ", "
                    str += artist.name

            return str

    class Playlist:
        def __init__(self, json):
            self.name = json["name"]
            self.tracks = []

            for t in json["tracks"]["items"]:
                self.tracks.append(Spotify.Track(t["track"]))

        def print(self):
            print(self.name)
            for t in self.tracks:
                print("\t", end="")
                t.print()

    class Album:
        def __init__(self, json):
            self.name = json["name"]
            self.tracks = []

            for t in json["tracks"]["items"]:
                self.tracks.append(Spotify.Track(t))


    def __init__(self):
        with open(self.CREDS_FILE) as f:
            j = json.load(f)
            self.sp = spotipy.Spotify(
                auth_manager=SpotifyOAuth(
                    client_id=j["client_id"],
                    client_secret=j["client_secret"],
                    redirect_uri=j["redirect_url"],
                    scope="user-library-read"
                )
            )

    def get_playlist_by_link(self, link: str) -> Playlist:
        json = self.sp.playlist(link)
        return Spotify.Playlist(json)

    def get_album_by_link(self, link: str) -> Album:
        json = self.sp.album(link)
        return Spotify.Album(json)


# Downloads URL to .tmp.mp3
def youtube_to_mp3(url: str):
    YDL_OPTS = {
        'format': 'bestaudio',
        'cookiesfrombrowser': ('firefox',),
        'extractaudio': True,
        'outtmpl': ".tmp.webm"
    }

    with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
        ydl.download([url])

    subprocess.run('ffmpeg -i .tmp.webm .tmp.mp3', shell=True)
    os.remove(".tmp.webm")

def youtube_search(query: str):
    # Options for searching
    ydl_opts = {
        'quiet': True,  # Suppress unnecessary output
        'extract_flat': True,  # Do not download videos, just extract info
        'force_generic_extractor': True,  # Use the generic extractor for all URLs
    }
    
    # Perform the search
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(f"ytsearch:{query}", download=False)
        # Print the first result
        video = result['entries'][0]  # First result
        #print(video)
        return f"https://www.youtube.com/watch?v={video['id']}"

spot = Spotify()

#p = spot.get_playlist_by_link("https://open.spotify.com/playlist/2hFAnErU2cPxkoxivmBT2l?si=1be60dd1bf6f4bac")
a = spot.get_album_by_link("https://open.spotify.com/album/7yQtjAjhtNi76KRu05XWFS?si=QYj0ot_STVC59v2DN9W1cw")

for i in range(len(a.tracks)):
    t = a.tracks[i]

    s = t.get_search_string()
    url = youtube_search(s)
    youtube_to_mp3(url)

    os.rename(".tmp.mp3", f"{t.track_number}. {t.name}")

#print(p.tracks[0].get_search_string())
#
#url = youtube_search(p.tracks[0].get_search_string())
#
#youtube_to_mp3(url)
#
#os.rename(".tmp.mp3", f"\"{p.tracks[0].get_search_string()}.mp3\"")

#for t in p.tracks:
    #print(t.get_search_string())

#youtube_search("andrew dotson")

#URL = "https://www.youtube.com/watch?v=KnlZ9qX7nz8"
#youtube_to_mp3(URL)

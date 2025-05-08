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


# Downloads URL to .tmp.mp3
def youtube_to_mp3(url: str):
    YDL_OPTS = {
        'format': 'bestaudio',
        'cookiesfrombrowser': ('firefox',),
        'extractaudio': True,
        'outtmpl': ".tmp.webm"
    }

    with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
        ydl.download([URL])

    subprocess.run('ffmpeg -i .tmp.webm .tmp.mp3', shell=True)
    os.remove(".tmp.webm")


spot = Spotify()

p = spot.get_playlist_by_link("https://open.spotify.com/playlist/2hFAnErU2cPxkoxivmBT2l?si=1be60dd1bf6f4bac")

for t in p.tracks:
    print(t.get_search_string())

URL = "https://www.youtube.com/watch?v=KnlZ9qX7nz8"
youtube_to_mp3(URL)

import json
import os
import subprocess

import spotipy
from spotipy.oauth2 import SpotifyOAuth

import yt_dlp

import music_tag

import requests


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

    class Image:
        def __init__(self, json):
            self.width = json["width"]
            self.height = json["height"]
            self.url = json["url"]

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
            self.release_year = json["release_date"]
            self.track_count = json["total_tracks"]

            self.images = []
            self.tracks = []
            self.artists = []

            for t in json["tracks"]["items"]:
                self.tracks.append(Spotify.Track(t))

            for a in json["artists"]:
                self.artists.append(Spotify.Artist(a))

            for i in json["images"]:
                self.images.append(Spotify.Image(i))

        def download(self):
            os.system(f"mkdir -p \"out/{self.name}\"")

            # Get album art
            img_data = None

            for image in self.images:
                if image.width ==  64 and image.height == 64:
                    img_data = requests.get(image.url).content

            if img_data == None:
                print("UNABLE TO GET ALBUM ART")
                exit()

            for i in range(len(self.tracks)):
                track = self.tracks[i]

                # Search youtube for track
                search = track.get_search_string()
                url = youtube_search(search)

                # Download to mp3 file
                dst = f"out/{self.name}/{str(track.track_number).zfill(len(str(self.track_count)))}. {track.name}"
                youtube_to_mp3(url, dst)
                
                # Create string of artists
                artists = self.artists[0].name
                for artist in self.artists[1:]:
                    artists += "/"
                    artists += artist.name

                # Add metadata to mp3
                mp3 = music_tag.load_file(f"{dst}.mp3")
                mp3["title"] = track.name
                mp3["album"] = self.name
                mp3["artist"] = artists
                mp3["discnumber"] = track.track_number
                mp3["year"] = self.release_year
                if img_data:
                    mp3["artwork"] = img_data
                mp3.save()
    

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
def youtube_to_mp3(url: str, dst: str):
    YDL_OPTS = {
        'format': 'bestaudio',
        'cookiesfrombrowser': ('firefox',),
        'extractaudio': True,
        'outtmpl': f"{dst}.webm"
    }

    with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
        ydl.download([url])

    subprocess.run(f"ffmpeg -i \"{dst}.webm\" \"{dst}.mp3\"", shell=True)
    os.remove(f"{dst}.webm")

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

a = spot.get_album_by_link("https://open.spotify.com/album/7yQtjAjhtNi76KRu05XWFS?si=QYj0ot_STVC59v2DN9W1cw")
a.download()

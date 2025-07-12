# SpotifyToMp3
This Python script takes Spotify playlists and albums and downloads them from youtube to an mp3 file. It uses yt-dlp to download the videos, the Spotify API for finding the albums and playlists, FFMPEG for converting formats, and music_tag for some metadata bits and pieces.

## Prerequesites
- Install the PIP packages. It's important to download yt-dlp from github directly because Youtube regularly implements changes to stop ytdlp from downloading, so they must regularly update to fix this.
``` bash
pip install -U git+https://github.com/yt-dlp/yt-dlp.git
pip install spotipy
pip install music_tag
```

- Install FFMPEG
```
sudo apt install ffmpeg
```
(or something similar for your distro)

- Generate Spotify API credentials and save them in a file called "spotify_credentials.json" in the same directory at stmp3.py. You can find out how to do that here: https://developer.spotify.com/documentation/web-api/concepts/authorization. You need to do this otherwise all the requests would come to MY API key, and that would probably be bad.

## Usage
```
python3 stmp3.py <link>
python3 stmp3.py <filepath>
```

Run the script from the same directory the python file is located in. This is because I haven't made sure it will work if you don't.

The link can either be a Spotify album or playlist link. You should get this by right clicking the album or playlist on the Spotify app, hovering over share, and selecting "Copy Album/Playlist Link". It should look something like this "https://open.spotify.com/album/4Gfnly5CzMJQqkUFfoHaP3?si=IWraXUxJRPOU66lSd11lqg". The file path is passed straight into Python's open so anything that will work there will work here (i.e. absolute or relative paths are both okay, but be careful using any sort of alias like ~ or $HOME). The file should contain the same type of links, one on each line, with no other extra characters (i.e. numbering or whitespace).

The songs will be downloaded to a new out/ directory which will be created in the same directory that stmp3.py is located.

Enjoy!

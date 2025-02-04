import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from urllib.parse import urlparse
from pprint import pprint

class SpotifyClient():
    
        def __init__(self, config):
            self.config = config
            self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config["spotify_client_id"],
                                                                client_secret=config["spotify_client_secret"],
                                                                redirect_uri=config["spotify_redirect_uri"],
                                                                scope=config["spotify_scope"]))
    
        # search songs by name and return the first result
        def searchSong(self, songName, slimit=1):
            results = self.sp.search(q=songName, limit=slimit)
            return results
        
        def getSong(self, songName):
            if songName.startswith("spotify:"):
                return self.sp.track(songName)
            elif songName.startswith("https://open.spotify.com/"):
                return self.sp.track(self.getSongUriFromUrl(songName))
            else:
                return self.searchSong(songName, slimit=1)
            
        def getSongUriFromUrl(self, songUrl):
            songId = urlparse(songUrl).path.split("/")[-1]
            songUri = "spotify:track:" + songId
            return songUri
    
        def addSongToQueue(self, songObject):
            try:
                self.sp.add_to_queue(songObject["tracks"]["items"][0]["uri"])
                return songObject["tracks"]["items"][0]["artists"][0]["name"] + " - " + songObject["tracks"]["items"][0]["name"]
            except:
                return False
            
        def addSongToPlaylist(self, songObject, playlistId):
            try:
                self.sp.playlist_add_items(playlistId, [songObject["tracks"]["items"][0]["uri"]])
                return songObject["tracks"]["items"][0]["artists"][0]["name"] + " - " + songObject["tracks"]["items"][0]["name"]
            except:
                return False
            
        def getQueue(self, limit=10):
            results = self.sp.queue()

            songlist = []
            for i in range(limit):
                artists = results["queue"][i]["artists"][0]["name"]
                for artist in results["queue"][i]["artists"]:
                    if artist["name"] != artists:
                        artists += ", " + artist["name"]
                songlist.append(artists + " - " + results["queue"][i]["name"])
            return songlist
        
        def getCurrentSong(self):
            results = self.sp.currently_playing()
            pprint(results)
            return results["item"]["artists"][0]["name"] + " - " + results["item"]["name"]
        
        def getLastSongs(self, limit=10):
            results = self.sp.current_user_recently_played(limit=limit)

            songlist = []
            for i in range(limit):
                artists = results["items"][i]["track"]["artists"][0]["name"]
                for artist in results["items"][i]["track"]["artists"]:
                    if artist["name"] != artists:
                        artists += ", " + artist["name"]
                songlist.append(artists + " - " + results["items"][i]["track"]["name"])
            return songlist
        
        def searchInPlaylist(self, songObject, playlistId):
            offset = 0
            limit = 100  # Maximum allowed by Spotify API
            song_found = False

            while True:
                results = self.sp.playlist_items(playlistId, limit=limit, offset=offset)
                total = results['total']

                for item in results['items']:
                    # Assuming songObject is the name of the song
                    if item['track']['id'] == songObject['tracks']['items'][0]['id']:
                        song_found = True
                        break

                if song_found or offset >= total:
                    break

                offset += limit

            return song_found
        
        def skipSong(self):
            self.sp.next_track()
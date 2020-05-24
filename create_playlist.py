"""
1. Take artists as input or read users top artists
2. See if artists have any new songs past specified date
3. If yes, add songs to playlist (either new or a specified playlist)
"""

import json
import requests
from secrets import spotify_user_id, spotify_token

class CreatePlaylist:

    def __init__(self):
        self.all_song_info = {}

    def get_artists(self):
        pass

    def check_new(self, artist_ids):
        for artist_id in artist_ids:
            query = "https://api.spotify.com/v1/artists/{id}/albums".format(artist_id)
            response = requests.post(
                query,
                data=request_body,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(spotify_token)
                }
            )

            response_json = response.json()
            albums = response_json['albums']['items']['id']
            #Cut ['id']?

            for album_id in albums:
                query = "https://api.spotify.com/v1/albums/{id}".format(album_id)
                response = requests.post(
                    query,
                    data=request_body,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": "Bearer {}".format(spotify_token)
                    }
                )

                response_json = response.json()
                albums = response_json['albums']['items']

    def create_playlist(self):

        request_body = json.dumps({
            "name": "Personalized New Music Playlist",
            "description": "New music from YOUR artists.",
            "public": False
        })

        query = "https://api.spotify.com/v1/users/{user_id}/playlists".format(spotify_user_id)
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type":"application/json",
                "Authorization":"Bearer {}".format(spotify_token)
            }
        )

        response_json = response.json()

        return response_json['id']

    def add_songs(self):
        pass
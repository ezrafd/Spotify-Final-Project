"""
1. Take artists as input or read users top artists
2. See if artists have any new songs past specified date
3. If yes, add songs to playlist (either new or a specified playlist)
"""

import json
import requests
from secrets import spotify_user_id, spotify_token
import datetime
import time

def main():
    cp = CreatePlaylist('2020-05-15')
    artist_ids = cp.get_artists(['Gunna', 'Polo G'])
    new = cp.check_new(artist_ids)

    #cp.create_playlist()


class CreatePlaylist:

    def __init__(self, cutoff_date):
        self.cutoff_date = datetime.datetime.strptime(cutoff_date, '%Y-%m-%d')

    def get_artists(self, artists):
        artist_ids = []
        for artist in artists:
            query = "https://api.spotify.com/v1/search?q={artist}&type=artist&limit=1".format(artist=artist)
            response = requests.get(
                query,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(spotify_token)
                }
            )

            response_json = response.json()
            print(response_json)
            artist_ids.append(response_json['artists']['items'][0]['id'])
        return artist_ids

    def check_new(self, artist_ids):
        albums = self.find_albums(artist_ids)
        new_albums = self.check_release_date(albums, self.cutoff_date)
        return new_albums

    def find_albums(self, artist_ids):
        albums = []
        for artist_id in artist_ids:
            query = "https://api.spotify.com/v1/artists/{id}/albums".format(id=artist_id)
            response = requests.get(
                query,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(spotify_token)
                }
            )

            response_json = response.json()
            print(response_json)
            for i in range(len(response_json['items'])):
                artist_albums = response_json['items'][i]['id']
                albums.append(artist_albums)

        return albums

    def check_release_date(self, albums, cutoff):
        album_release_dates = []
        for album_id in albums:
            query = "https://api.spotify.com/v1/albums/{id}".format(id=album_id)
            response = requests.get(
                query,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(spotify_token)
                }
            )

            response_json = response.json()
            rd = datetime.datetime.strptime(response_json['release_date'], '%Y-%m-%d')
            album_release_dates.append(rd)

        new_albums = []
        for i, date in enumerate(album_release_dates):
            if date >= cutoff:
                new_albums.append(albums[i])

        return new_albums

    def create_playlist(self):

        request_body = json.dumps({
            "name": "Personalized New Music Playlist",
            "description": "New music from YOUR artists.",
            "public": False
        })

        query = "https://api.spotify.com/v1/users/{user_id}/playlists".format(user_id=spotify_user_id)
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

if __name__ == '__main__':
    main()
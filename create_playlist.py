"""
1. Take artists as input or read users top artists
2. See if artists have any new songs past specified date
3. If yes, add songs to playlist (either new or a specified playlist)
"""

import json
import requests
from secrets import spotify_user_id, spotify_token
import datetime

def main():
    cp = CreatePlaylist(['Polo G', 'Lil Durk'], '2020-01-01')
    artist_ids = cp.get_artists()
    new = cp.check_new(artist_ids)
    playlist = cp.create_playlist()
    songs = cp.get_songs(new)
    cp.add_songs(playlist, songs)


class CreatePlaylist:

    def __init__(self, artist_names, cutoff_date):
        self.cutoff_date = datetime.datetime.strptime(cutoff_date, '%Y-%m-%d')
        self.artists = artist_names

    def get_artists(self):
        artist_ids = []
        for artist in self.artists:
            query = "https://api.spotify.com/v1/search?q={artist}&type=artist&limit=1".format(artist=artist)
            response = requests.get(
                query,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(spotify_token)
                }
            )

            response_json = response.json()
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
        artist_names = ", ".join(self.artists)

        request_body = json.dumps({
            "name": "Personalized New Music Playlist",
            "description": "New music from YOUR artists: {}".format(artist_names),
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

    def get_songs(self, new_albums):
        songs = []
        song_names = []
        for album_id in new_albums:
            query = "https://api.spotify.com/v1/albums/{id}/tracks".format(id=album_id)
            response = requests.get(
                query,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(spotify_token)
                }
            )

            response_json = response.json()

            for i in range(len(response_json['items'])):
                if response_json['items'][i]['name'] in song_names:
                    break

                for artist in self.artists:
                    for j in range(len(response_json['items'][i]['artists'])):
                        if artist == response_json['items'][i]['artists'][j]['name'] and \
                                response_json['items'][i]['name'] not in song_names:
                            uri = response_json['items'][i]['uri']
                            songs.append(uri)
                            song_names.append(response_json['items'][i]['name'])

        return songs

    def add_songs(self, playlist, songs):
        # add all songs into new playlist
        request_data = json.dumps(songs)

        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist)

        response = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )

        response_json = response.json()
        return response_json


if __name__ == '__main__':
    main()
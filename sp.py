import json
from requests_oauthlib import OAuth2Session
import requests
import base64
import  urllib.parse as urlparse
from urllib.parse import parse_qs

from secrets import sp_client_id, sp_client_secret

import artist_track_extract


client_id = sp_client_id
client_secret = sp_client_secret
redirect_uri = 'https://www.spotify.com'
scope = "playlist-modify-public user-read-email user-read-private playlist-modify-private"
req = f'{client_id}:{client_secret}'
encoded = base64.b64encode(req.encode())

class sp :
    def __init__(self) :
        self.uri_list = []
        self.get_token()
        self.get_id()
        self.create_playlist()
        self.search()
        self.add_items()


    def get_token(self) :
        url = 'https://accounts.spotify.com/authorize'
        oauth = OAuth2Session(client_id, redirect_uri = redirect_uri, scope = scope)
        authorization_url, state = oauth.authorization_url(url)
        print(authorization_url)
        authorization_response = input('paste here : ')

        parsed = urlparse.urlparse(authorization_response)
        authorization_code = parse_qs(parsed.query)['code'][0]

        # to get auth token
        headers = {
            'Authorization' : f'Basic {encoded.decode()}'
        }
        data = {
            'grant_type' : 'authorization_code',
            'redirect_uri' : redirect_uri,
            'code' : authorization_code
        }

        access = requests.post('https://accounts.spotify.com/api/token', data = data, headers = headers)
        response = json.loads(access.text)
        self.access_token = response['access_token']

    def get_id(self) :
        headers = {
            'Authorization' : f'Bearer {self.access_token}'
        }
        user_info = requests.get('https://api.spotify.com/v1/me', headers = headers)
        user_info.raise_for_status()
 

        user_info = json.loads(user_info.text)
        self.user_id  = user_info['id']

    def search(self) :
        
        search_url = 'https://api.spotify.com/v1/search'

        track_data_list = artist_track_extract.get_data(input('Enter youtube playlist url :'))
        
        for song_details in track_data_list :

            headers = {
                'Authorization': f'Bearer {self.access_token}'
            }
            params = {
                'q' : f"track:{song_details['track_name']} artist:{song_details['artist']}", 
                'type' : 'track',
                'limit' : 1,

            }

            search_response = requests.get(search_url, headers = headers, params = params)
            search_response.raise_for_status()
            
            json_response = search_response.json()
            try :
                song_uri =  json_response['tracks']['items'][0]['uri']
                print(f'Song found : {song_details["track_name"]}')
                self.uri_list.append(song_uri)
            except IndexError :
                print(f'Song {song_details["track_name"]} not found')
        
    def create_playlist(self) :
        create_playlist_url = f'https://api.spotify.com/v1/users/{self.user_id}/playlists'

        headers = {
            'Authorization' : f'Bearer {self.access_token}',
            'Content-Type' : 'application/json'
        }

        data = json.dumps({
            'name' : input('Enter name of your new playlist :')
        })
        response = requests.post(create_playlist_url, headers = headers, data = data)
        print(response)
        self.playlist_id = response.json()['id']
        print(self.playlist_id)

    def add_items(self) :

        add_items_url = f'https://api.spotify.com/v1/playlists/{self.playlist_id}/tracks'

        headers = {
            'Authorization' : f'Bearer {self.access_token}',
            'Content-Type' : 'application/json'
        }
        print(self.uri_list)
        data = {
            'uris' : self.uri_list
        }

        res = requests.post(add_items_url, headers = headers, data = json.dumps(data))
        print(res)

if __name__ == '__main__' :

    user = sp()



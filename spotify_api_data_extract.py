import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

#For Authentication
client_credentials_manager = SpotifyClientCredentials(client_id="499004a61eb34a05bf0b2d41596b601e", client_secret="5c84bccd202d46c0ab934a560cbd487f")

#For Authorization
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

#Get the playlist ID for top songs
playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=1333723a6eff4b7f"
playlist_URI = playlist_link.split("/")[-1].split("?")[0]
data = sp.playlist_tracks(playlist_URI)

#Get the album details
album_list = []
for row in data['items']:
    album_id = row['track']['album']['id']
    album_name = row['track']['album']['name']
    album_release_date = row['track']['album']['release_date']
    album_total_tracks = row['track']['album']['total_tracks']
    album_url = row['track']['album']['external_urls']['spotify']
    album_element = {'album_id': album_id, 'name': album_name, 'release_date': album_release_date,
                     'total_tracks': album_total_tracks, 'url': album_url}
    album_list.append(album_element)

#Get the artist details
artist_list = []
for row in data['items']:
    for key, value in row.items():
        if key == "track":
            for artist in value['artists']:
                artist_dict = {'artist_id':artist['id'], 'artist_name':artist['name'], 'external_url': artist['href']}
                artist_list.append(artist_dict)

#Get the song details
song_list = []
for row in data['items']:
    song_id = row['track']['id']
    song_name = row['track']['name']
    song_duration = row['track']['duration_ms']
    song_url = row['track']['external_urls']['spotify']
    song_popularity = row['track']['popularity']
    song_added = row['added_at']
    album_id = row['track']['album']['id']
    artist_id = row['track']['album']['artists'][0]['id']
    song_element = {'song_id':song_id,'song_name':song_name,'duration_ms':song_duration,'url':song_url,
                    'popularity':song_popularity,'song_added':song_added,'album_id':album_id,
                    'artist_id':artist_id
                   }
    song_list.append(song_element)

#Create dataframe and convert the datatype
album_df = pd.DataFrame.from_dict(album_list)
album_df = album_df.drop_duplicates(subset=['album_id'])
artist_df = pd.DataFrame.from_dict(artist_list)
artist_df = artist_df.drop_duplicates(subset=['artist_id'])
song_df = pd.DataFrame.from_dict(song_list)
album_df['release_date'] = pd.to_datetime(album_df['release_date'])
song_df['song_added'] =  pd.to_datetime(song_df['song_added'])
print(song_df.info())

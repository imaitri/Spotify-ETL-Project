import json
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import boto3
from datetime import datetime

def lambda_handler(event, context):
    # TODO implement
    #For Authentication
    client_id = os.environ.get('client_id')
    client_secret = os.environ.get('client_secret')
    client_credentials_manager = SpotifyClientCredentials(client_id="499004a61eb34a05bf0b2d41596b601e", client_secret="5c84bccd202d46c0ab934a560cbd487f")
#client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)

#For Authorization
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

#Get the playlist ID for top songs
    playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=1333723a6eff4b7f"
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]
    data = sp.playlist_tracks(playlist_URI)
    print(data)
    
    
    cilent = boto3.client('s3')
    
    filename = "spotify_raw_" + str(datetime.now()) + ".json"
    
    cilent.put_object(
        Bucket="spotify-etl-project-maitri",
        Key="raw_data/to_processed/" + filename,
        Body=json.dumps(data)
        )



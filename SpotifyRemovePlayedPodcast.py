# 1. Read secrect.json
# 2. Access Spotify account
# 3. Get list of playlists
# 4. Remove played podcasts from selected playlist

import json
import spotipy

ID = "123"
SECRET = "123"
username = "name"
scope = "user-read-playback-position playlist-modify-public playlist-modify-private"


def read_secret():
    with open('secret.json') as json_file:
        data = json.load(json_file)
        c_ID = data['client_id']
        c_SECRET = data['client_secret']
        c_username = data['username']

    return c_ID, c_SECRET, c_username

def spotify_authentication():
    token = spotipy.util.prompt_for_user_token(username, scope, client_id=ID,client_secret=SECRET,redirect_uri='https://developer.spotify.com/dashboard/applications/8d942323bbf04dbfa2ab234d777f5200')

    sp = spotipy.Spotify(auth=token)

    return sp

def get_playlist(sp):
    playlists = sp.user_playlists(username)

    sp_playlist_name = []
    sp_playlist_id = []

    for playlist in playlists['items']:
        sp_playlist_name.append(playlist['name'])
        sp_playlist_id.append(playlist['id'])

    # Select the playlist
    i = 0
    for i in range(len(sp_playlist_name)):
        print (str(i) + " - " + sp_playlist_name[i])
        i = i + 0

    select_list = input("Select the playlist to use: ")

    return sp_playlist_id[int(select_list)]

def episode_played(sp, playlist_id, episodes):
    episodes_to_remove = []

    for episode in episodes['items']:
        episode_id = episode['track']['uri']

        r = sp.episode(episode_id)
        played = r['resume_point']['fully_played']
        
        if (played == True):
            episodes_to_remove.append(episode_id)
            
    #print(episodes_to_remove)
    sp.playlist_remove_all_occurrences_of_items(playlist_id, episodes_to_remove)

    return

if __name__ == '__main__':
    json_secret = read_secret()
    ID = json_secret[0]
    SECRET = json_secret[1]
    username = json_secret[2]

    # Authenticte with Spotify
    sp = spotify_authentication()

    # Get all of the available playlists
    ava_playlists = get_playlist(sp)

    # Get the tracks in the playlist
    results = sp.playlist_items(ava_playlists)
    #print (json.dumps(results, indent=4))
    
    episode_played(sp, ava_playlists, results)


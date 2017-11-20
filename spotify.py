import sys
import spotipy
import spotipy.util as util
import time
import keys


def gettoken():
    scope = keys.spotifyscope
    token = util.prompt_for_user_token(keys.spotifyusername, scope, client_id=keys.spotifyclientid,client_secret=keys.spotifyclientsecret,redirect_uri=keys.redirecturl)
    return token


def current(token):
    sp = spotipy.Spotify(auth=token)
    current = {'current': None}

    try:
        data = sp.current_user_playing_track()
    except:
        data = None

    if data:
        item = data['item']
        title = item['name']
        artist = item['artists'][0]['name']
        album = item['album']['name']
        time = (data['progress_ms']/1000)
        playing = data['is_playing']
        # Preview = i['preview_url']
        result = {'title': title, 'artist': artist, 'album': album, 'progress': time, 'playing': playing}
        current.update({'current': result})
    return current


def recent(token):
    sp = spotipy.Spotify(auth=token)
    data = sp.current_user_recently_played(limit = 25)
    recent = {}
    results = []

    for i in data['items']:
        track = i['track']
        title = track['name']
        artist = track['artists'][0]['name']
        album = track['album']['name']
        played_at = i['played_at']
        # Preview = i['preview_url']
        results.append({'title': title, 'artist': artist, 'album': album, 'timestamp': played_at})
    recent.update({'recent': results})
    return recent

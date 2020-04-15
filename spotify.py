import sys
import spotipy
import spotipy.util as util
import time
import keys


def gettoken():
    scope = keys.spotifyscope
    token = util.prompt_for_user_token(keys.spotifyusername, scope, client_id=keys.spotifyclientid,client_secret=keys.spotifyclientsecret,redirect_uri=keys.redirecturl)
    return token


def recent(token, reformat):
    sp = spotipy.Spotify(auth=token)
    data = sp.current_user_recently_played(limit = 25)
    recent = {}
    results = []

    index = 0
    for i in data['items']:
        item = i['track']
        track = item['name']
        artist = item['artists'][0]['name']
        album = item['album']['name']
        played_at = i['played_at']
        track_link = item['external_urls']['spotify']
        artist_link = item['artists'][0]['external_urls']['spotify']
        # Preview = i['preview_url']
        results.append({'track': track, 'artist': artist, 'album': album, 'track_link': track_link, 'artist_link': artist_link, 'timestamp': played_at})

        if reformat == 'sentence':
            results[index] = track + ' by ' + artist
            index = index + 1

    recent.update({'recent': results})
    return recent


def current(token, reformat):
    sp = spotipy.Spotify(auth=token)
    current = {'current': None}

    try:
        data = sp.current_user_playing_track()
    except:
        data = None

    if data:
        item = data['item']
        track = item['name']
        artist = item['artists'][0]['name']
        album = item['album']['name']
        track_link = item['external_urls']['spotify']
        artist_link = item['artists'][0]['external_urls']['spotify']
        # progress = int(data['progress_ms'] / (item['duration_ms']*1.00) * 100)
        playing = data['is_playing']
        # Preview = i['preview_url']
        result = {'track': track, 'artist': artist, 'album': album, 'playing': playing, 'track_link': track_link, 'artist_link': artist_link}

        if reformat == 'sentence':
            result = track + ' by ' + artist

        current.update({'current': result})
    return current

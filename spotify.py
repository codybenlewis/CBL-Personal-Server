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
        track = i['track']
        title = track['name']
        artist = track['artists'][0]['name']
        album = track['album']['name']
        played_at = i['played_at']
        link = track['external_urls']['spotify']
        # Preview = i['preview_url']
        results.append({'title': title, 'artist': artist, 'album': album, 'link': link, 'timestamp': played_at})

        if reformat == 'sentence':
            results[index] = title + ' by ' + artist
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
        title = item['name']
        artist = item['artists'][0]['name']
        album = item['album']['name']
        link = item['external_urls']['spotify']
        # progress = int(data['progress_ms'] / (item['duration_ms']*1.00) * 100)
        playing = data['is_playing']
        # Preview = i['preview_url']
        result = {'title': title, 'artist': artist, 'album': album, 'playing': playing, 'link': link}

        if reformat == 'sentence':
            result = title + ' by ' + artist

        current.update({'current': result})
    return current

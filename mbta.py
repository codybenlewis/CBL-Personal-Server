import requests
import keys


def collect_data(station):
    keyconvert = station.lower()
    if keyconvert == 'kenmore':
        station = 'place-kencl'
        lines = 1
    elif keyconvert == 'hynes' or keyconvert == 'hynesconventioncenter':
        station = 'place-hymnl'
        lines = 1
    elif keyconvert == 'copley':
        station = 'place-coecl'
        lines = 1
    elif keyconvert == 'arlington':
        station = 'place-armnl'
        lines = 1
    elif keyconvert == 'boylston':
        station = 'place-boyls'
        lines = 1
    elif keyconvert == 'parkst' or keyconvert == 'parkstreet':
        station = 'place-pktrm'
        lines = 2
    elif keyconvert == 'govcenter' or keyconvert == 'governmentcenter':
        station = 'place-gover'
        lines = 2
    else:
        return False
    parameters = {'api_key': keys.mbtaapikey, 'stop': station,'format': 'json'}
    # Get the predictionsbystop data with the given Kenmore parameters
    response = requests.get("http://realtime.mbta.com/developer/api/v2/predictionsbystop", params=parameters)
    source = response.json()
    return source


def filter_data(source, direction):
    try:
        data = source['mode']
    except:
        return

    data = data[0]['route']

    if data:
        results = []
        for i in data:
            for j in i['direction']:
                if j['direction_name'] == direction:
                    for k in j['trip']:
                        train = {'line':i['route_id'], 'name':k['trip_headsign'], 'time':int(k['pre_away'])//60}
                        results.append(train)
        if results:
            return sorted(results, key=lambda k: k['time'])
        return
    return


def dejson(results):
    if results:
        results_list = []
        for i in results:
            train = [str(i['line']), str(i['name']), i['time']]
            results_list.append(train)
        return results_list
    return


def format_entries(results, spaces):
    if results:
        limit = spaces
        for index in range(len(results)):
            if results[index][1] == 'Boston College':
                results[index][1] = 'Boston Col'
            elif results[index][1] == 'Cleveland Circle':
                results[index][1] = 'Clvlnd Cir'
            elif results[index][1] == 'Heath Street':
                results[index][1] = 'Heath St'
            elif results[index][1] == 'Park Street':
                results[index][1] = 'Park St'
            elif results[index][1] == 'Government Center':
                results[index][1] = "Gov't Ctr"
            elif results[index][1] == 'North Station':
                results[index][1] = 'North Sta'

            if results[index][2] == 0:
                results[index][2] = 'ARR'
            else:
                results[index][2] = str(results[index][2]) + 'Min'

            itemlen = len(results[index][1])  + len(results[index][2])
            results[index] = (results[index][1] + (' ' * (limit - itemlen)) + results[index][2])
        return results
    return



def compile_data(source, direction, reformat):
    results = filter_data(source, direction)
    if reformat:
        if reformat == 'lcd':
            results = dejson(results)
            results = format_entries(results, 16)
    return results

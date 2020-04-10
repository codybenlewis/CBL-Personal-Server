from flask import Flask, jsonify, request, render_template, Markup
import mbta
import spotify
import lights
import keys


app = Flask(__name__)

#
#
#   GENERAL FUNCTIONS
#
#


def directory(error_input = None, filename = 'index.html'):
    if error_input == None:
        return render_template(filename)
    return render_template(filename, error = Markup('<b>Error:</b> ') + error_input + 'Hello, Lady!')


def validate(entry, password):
    if entry.lower() == password:
        return True
    return False


#
#
#   INDEX PAGE
#
#


@app.route('/')
def index():
    return render_template('index.html')


#
#
#   LIGHTS
#
#


@app.route('/lights/', methods=['GET'])
def lightsindex():
    password = request.args.get('password', default="")
    if validate(password, keys.lightspassword):
        return render_template('lights.html', key = password)
    return directory('Invalid password. ', 'index.html')


@app.route('/lights/on', methods=['GET'])
def lightson():
    password = request.args.get('password', default="")
    if validate(password, keys.lightspassword):
        result = {}
        state = lights.on()
        return jsonify({'state': state.lower()})
    return directory('Invalid password. ', 'index.html')


@app.route('/lights/off', methods=['GET'])
def lightsoff():
    password = request.args.get('password', default="")
    if validate(password, keys.lightspassword):
        result = {}
        state = lights.off()
        return jsonify({'state': state.lower()})
    return directory('Invalid password. ', 'index.html')


@app.route('/lights/invert', methods=['GET'])
def lightsinvert():
    password = request.args.get('password', default="")
    if validate(password, keys.lightspassword):
        result = {}
        state = lights.invert()
        #return ('The Lights Are ' + state.capitalize() + '.')
        return jsonify({'state': state.lower()})
    return directory('Invalid password. ', 'index.html')


#
#
#   Soundboard
#
#


@app.route('/soundboard/')
def soundboard():
    return render_template('soundboard.html')


#
#
#   SPOTIFY
#
#


@app.route('/spotify/')
def spotifyindex():
    return render_template('spotify.html')


@app.route('/spotify/recent', methods=['GET'])
def spotifyrecent():
    reformat = request.args.get('format', default=False)
    token = spotify.gettoken()

    if reformat:
        reformat = reformat.lower()
        if reformat != 'sentence':
            return directory('Invalid Format. ', 'spotify.html')

    if token:
        results = {}
        results.update(spotify.recent(token, reformat))
        return jsonify(results)
    return directory('No Token Returned', 'spotify.html')


@app.route('/spotify/current', methods=['GET'])
def spotifycurrent():
    reformat = request.args.get('format', default=False)
    token = spotify.gettoken()

    if reformat:
        reformat = reformat.lower()
        if reformat != 'sentence':
            return directory('Invalid Format. ', 'spotify.html')

    if token:
        results = {}
        results.update(spotify.current(token, reformat))
        return jsonify(results)
    return directory('No Token Returned. ', 'spotify.html')


#
#
#   MBTA
#
#


@app.route('/mbta/')
def mbtaindex():
    return directory(None, 'mbta.html')


@app.route('/mbta/<station>', methods=['GET'])
def mbtastation(station=False):
    direction = request.args.get('direction', default=False)
    reformat = request.args.get('format', default=False)
    warning = 'Did you spell something wrong? '
    results = {}

    # Error handling if no station was specifed to overwrite the default value
    if station is False:
        return  directory('No Station Selected. ' + warning, 'mbta.html')

    # Error handling for False return from the collect data function
    source = mbta.collect_data(station)
    if source is False:
        return  directory('Invalid Station. ' + warning, 'mbta.html')

    # Error handling for incorrect format entry
    if reformat:
        reformat = reformat.lower()
        if reformat != 'lcd':
            return  directory('Invalid Format. ' + warning, 'mbta.html')

    if direction:
        direction = direction.lower()
        if direction == 'northbound' or direction == 'north':
            direction = 'Northbound'
            results.update({'northbound':mbta.compile_data(source, direction, reformat)})
            return jsonify(results)
        elif direction == 'southbound' or direction == 'south':
            direction = 'Southbound'
            results.update({'southbound':mbta.compile_data(source, direction, reformat)})
            return jsonify(results)
        elif direction == 'eastbound' or direction == 'east':
            direction = 'Eastbound'
            results.update({'eastbound':mbta.compile_data(source, direction, reformat)})
            return jsonify(results)
        elif direction == 'westbound' or direction == 'west':
            direction = 'Westbound'
            results.update({'westbound':mbta.compile_data(source, direction, reformat)})
            return jsonify(results)
        else:
            return directory('Invalid Direction. ' + warning, 'mbta.html')

    results.update({'westbound':mbta.compile_data(source, 'Westbound', reformat)})
    results.update({'eastbound':mbta.compile_data(source, 'Eastbound', reformat)})
    return jsonify(results)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)

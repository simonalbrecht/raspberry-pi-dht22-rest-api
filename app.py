#!flask/bin/python
import sys
import optparse
import datetime
import Adafruit_DHT
from flask import Flask, jsonify

app = Flask(__name__)
sensor_name = 'Sensor'
gpio_pin = 4

last_measurement = (None, None)
last_measurement_time = None

debug_mode = False
debug_measurement = (22.7, 32)

# http://flask.pocoo.org/snippets/133/
def flaskrun(app,
                  default_host='127.0.0.1', 
                  default_port='5000', 
                  default_sensor_name='Sensor',
                  default_gpio_pin=4):
    global sensor_name
    global gpio_pin
    global debug_mode

    parser = optparse.OptionParser()
    parser.add_option('-H', '--host',
                      help='Hostname of the Flask app ' + \
                           '[default %s]' % default_host,
                      default=default_host)
    parser.add_option('-P', '--port',
                      help='Port for the Flask app ' + \
                           '[default %s]' % default_port,
                      default=default_port)
    parser.add_option('-N', '--sensor-name',
                      help='The name of the sensor being read for measurements' + \
                           '[default %s]' % default_sensor_name,
                      default=default_sensor_name)
    parser.add_option('-G', '--gpio-pin',
                    help='The GPIO pin to which the sensor is connected' + \
                            '[default %s' % default_gpio_pin,
                            default=default_gpio_pin)
    parser.add_option('-d', '--debug',
                      action='store_true', dest='debug',
                      help=optparse.SUPPRESS_HELP)

    options, _ = parser.parse_args()

    sensor_name = options.sensor_name
    gpio_pin = options.gpio_pin
    debug_mode = options.debug

    app.run(debug=options.debug,
        host=options.host,
        port=int(options.port)
    )

def get_measurement():
    global last_measurement
    global last_measurement_time

    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, gpio_pin) if not debug_mode else debug_measurement
    
    last_measurement_time = datetime.datetime.now()
    last_measurement = (humidity, temperature)

    return last_measurement

@app.route('/api/v1/temperature', methods=['GET'])
def get_temperature():
    temperature = get_measurement()[1]
    return jsonify({
        'name': sensor_name, 
        'temperature': temperature, 
        'timestamp': last_measurement_time.isoformat()
    })

@app.route('/api/v1/humidity', methods=['GET'])
def get_humidity():
    humidity = get_measurement()[0]
    return jsonify({
        'name': sensor_name, 
        'humidity': humidity, 
        'timestamp': last_measurement_time.isoformat()
    })

@app.route('/api/v1/temperature+humidity', methods=['GET'])
def get_temperature_and_humidity():
    humidity, temperature = get_measurement()
    return jsonify({
        'name': sensor_name, 
        'temperature': temperature,
        'humidity': humidity, 
        'timestamp': last_measurement_time.isoformat()
    })

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')

    flaskrun(app)
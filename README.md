# DHT22 on Raspberry Pi as a REST API
This is a simple python (flask) application that exposes the values read from a DHT22 (connected to  Raspberry Pi GPIO) via a REST API.

Uses [Adafruit's DHT Library](https://github.com/adafruit/Adafruit_Python_DHT) to access the data on the GPIO.

## Installation
### Step 1: Virtualenv Setup
Create a virtualenv for our python stuff (to isolate from other python things):
```
virtualenv flask
```
If you do not have virtualenv installed, follow the instructions [here](https://virtualenv.pypa.io/en/stable/installation/).

### Step 2: Install DHT Library
Install the [DHT Library](https://github.com/adafruit/Adafruit_Python_DHT) using the flask virtual env:
```
 git clone https://github.com/adafruit/Adafruit_Python_DHT.git adafruit-python-dht
 cd adafruit-python-dht
 ../flask/bin/python setup.py install
 cd -
```

**TIP**: If you get an error during the last step, you are most likely not running it on supported hardware (Raspberry Pi/Beaglebone). To install it on unsupported hardware, you can use the `--force-test` flag.

## Step 3: Installation other dependencies
```
flask/bin/pip install -r requirements.txt
```

## Usage
To start the application, simply do:
```
./app.py
```

The following REST endpoints are exposed:
* [http://localhost:5000/api/v1/temperature](http://localhost:5000/api/v1/temperature)
* [http://localhost:5000/api/v1/humidity](http://localhost:5000/api/v1/humidity)
* [http://localhost:5000/api/v1/temperature+humidity](http://localhost:5000/api/v1/temperature+humidity)

## Configuration
This applicaiton assumes that the DHT22 data pin is pin *5* on the Raspberry GPIO. This setting can be changed by passing in the `--gpio-pin` command line parameter.

Alongside the `--gpio-pin` there are the following command line parameters available

| Flag | Description | Default |
| ---- | ----------- | ------- |
| `-H, --host` | Defines the host the application is exposed on. | `127.0.0.1` |
| `-P, --port` | Defines the port port the application is exposed on. | `5000` | 
| `-N, --sensor_name` | Defines the name of the sensor used in the `name` field in the API response. Can be used to set a unique name to better differentiate between multple sensors/instances. | `Sensor` |
| `-G, --gpio-pin` | Defines which pin will be accessed to read the DHT data | `4` |

## Run as a service
This assumes, that the repository was cloned to `/opt/simonalbrecht/raspberry-pi-dht22-rest-api/` and the virtualenv name is `flask`.

Copy the file `etc/systemd/system/dht22-rest-api@pi.service` to `/etc/systemd/system/` on the Raspberry Pi to which the DHT22 sensor is connected. Change the command line parameters (GPIO pin, sensor name, port etc) on the `ExecStart` line to match your setup.

Reload the systemd daemon to make it aware of the new service:
```
sudo systemctl --system daemon-reload
```

And finally, enable (start on boot automatically) and start it:
```
sudo systemctl enable dht22-rest-api@pi
sudo systemctl start dht22-rest-api@pi
```

To check the status of the service, use:
```
sudo systemctl status dht22-rest-api@pi
```

For the logs, run:
```
 sudo journalctl -f -u dht22-rest-api@pi
```

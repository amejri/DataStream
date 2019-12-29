import json
import time
import urllib.request

# Run `pip install kafka-python` to install this package
from kafka import KafkaProducer

API_KEY = "2b0492eff8eb9d000e0d6ba70a3202d35ac3b6ce" # FIXME
url = "https://api.jcdecaux.com/vls/v1/stations?apiKey={}".format(API_KEY)

producer = KafkaProducer(bootstrap_servers="localhost:9092")

available_bikes = {}
i=0
while True:
    response = urllib.request.urlopen(url)
    stations = json.loads(response.read().decode())
    for station in stations:
        current_available_bike = station['available_bikes']
        key = "{},{}".format(station["number"], station["contract_name"])
        if key not in available_bikes:
            available_bikes[key] = current_available_bike

        if ( current_available_bike == 0 and available_bikes[key] > 0 ) or \
           ( current_available_bike > 0 and available_bikes[key] == 0):

            print('station = ',station)
            producer.send("empty-stations",
                          json.dumps(station).encode())
            print()
        available_bikes[key] = current_available_bike

    time.sleep(1)
i += 1
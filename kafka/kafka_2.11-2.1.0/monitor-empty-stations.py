import json
from kafka import KafkaConsumer

empty_stations_per_city = {}

consumer = KafkaConsumer("empty-stations", bootstrap_servers='localhost:9092',
                         group_id="velib-monitor-stations")
for message in consumer:
    station = json.loads(message.value.decode())
    station_name = station["name"]
    station_address = station["address"]
    current_available = int(station["available_bikes"])
    station_city = station["contract_name"]


    if current_available == 0:
        print("- address=({}) - city=({}) become empty. ".format(station_address,station_city))
        print('')

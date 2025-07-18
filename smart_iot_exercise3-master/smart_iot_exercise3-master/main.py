"""
Filename: main.py
Author: Patrick Meyer
Date: 2024-11-25
Description: This script receives messages from mqtt and write datapoints in influxdb cloud.
used sources: 
Influxdata documentation (https://docs.influxdata.com/influxdb/cloud/api-guide/client-libraries/python/)
paho-mqtt project description (https://pypi.org/project/paho-mqtt/)
"""
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import json


# mqtt configuration
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "/sensor/data/SIOT" 

# InfluxDB configuration
INFLUXDB_URL = "https://eu-central-1-1.aws.cloud2.influxdata.com" 
INFLUXDB_TOKEN = "CHfiu7VdD4CJX_ThYw-iIZKMvSq60lbr9QYz8aeZWDaPH_z0jbTO_zrME5j0ggFs1XwZdl8-LPGnphhfOQ6zBg=="  
INFLUXDB_ORG = "Gruppe_01" 
INFLUXDB_BUCKET = "smart-iot" 

# connect to InfluxDB
influx_client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = influx_client.write_api(write_options=SYNCHRONOUS)

# callback when successfull connected to mqtt
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")
    client.subscribe(MQTT_TOPIC) 

# callback for received message from mqtt
def on_message(client, userdata, msg):
    print(f"Message received on topic {msg.topic}: {msg.payload.decode()}")
    try:
        
        data = json.loads(msg.payload.decode())
        count = data.get("count")
        
        if count is not None:
            counter_point = Point("PIR").tag("type","chicken_count").field("count", count)
            write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=counter_point)
            print(f"Counter data written to InfluxDB: {counter_point}")

    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
    except Exception as e:
        print(f"Error processing message: {e}")

# initialize the client
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# connecting to the broker
print("Connecting to MQTT Broker...")
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

#loop for incoming messages from mqtt
mqtt_client.loop_forever()  

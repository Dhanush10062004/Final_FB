import time
import paho.mqtt.client as paho
from paho import mqtt

# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid), str(userdata))


# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

# using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
# userdata is user defined data of any type, updated by user_data_set()
# client_id is the given name of the client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set("Dhanush_B", "@Dooon10@")
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect("85196a53c82e40649a72fe2ebf88dc64.s1.eu.hivemq.cloud", 8883)


client.on_message = on_message
client.on_publish = on_publish

# a single publish, this can also be done in loops, etc.
client.publish("test/topic", payload="hot", qos=1)

# loop_forever for simplicity, here you need to stop the loop manually
# you can also use loop_start and loop_stop
client.loop_forever()

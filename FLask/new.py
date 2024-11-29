from flask import Flask
from flask_socketio import SocketIO, emit
import paho.mqtt.client as mqtt
import ssl
import threading

# Flask app setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# MQTT setup
BROKER = "85196a53c82e40649a72fe2ebf88dc64.s1.eu.hivemq.cloud"  # HiveMQ broker address
PORT = 8883               # Secure MQTT port for TLS
TOPIC = "test/topic"      # MQTT topic
USERNAME = "Dhanush_B"    # HiveMQ username
PASSWORD = "@Dooon10@"    # HiveMQ password

# MQTT callback functions
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker successfully!")
        client.subscribe(TOPIC)
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    # Decode the MQTT message payload
    data = msg.payload.decode("utf-8")
    print(f"Received message: {data} on topic: {msg.topic}")
    
    # Emit data to frontend via WebSocket
    socketio.emit('mqtt_message', {'topic': msg.topic, 'message': data})

# Initialize MQTT client
mqtt_client = mqtt.Client()
mqtt_client.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2)  # Enable TLS with version 1.2
mqtt_client.username_pw_set(USERNAME, PASSWORD)       # Set HiveMQ credentials
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Connect to the MQTT broker
def start_mqtt():
    try:
        mqtt_client.connect(BROKER, PORT, keepalive=60)  # Attempt to connect
        mqtt_client.loop_forever()  # Keep the client loop running
    except Exception as e:
        print(f"Error connecting to MQTT broker: {e}")

# Flask route for testing
@app.route('/')
def index():
    return "MQTT to WebSocket bridge with HiveMQ is running."

# Start the MQTT loop before the Flask app
@socketio.on('connect')
def on_connect_socket():
    print("Frontend connected via WebSocket.")

# Main entry point
if __name__ == '__main__':
    # Run MQTT client loop in a separate thread
    mqtt_thread = threading.Thread(target=start_mqtt)
    mqtt_thread.daemon = True
    mqtt_thread.start()
    
    # Run Flask app with SocketIO
    socketio.run(app, host='0.0.0.0', port=5000)

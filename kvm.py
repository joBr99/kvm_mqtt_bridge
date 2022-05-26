import serial
import re
import time
from paho.mqtt import client as mqtt_client

broker = '192.168.75.30'
port = 1883
client_id = 'kvm_desk'
username = 'mqttuser'
password = 'password'

com = "/dev/ttyUSB0"

tty = serial.Serial(com, 19200)

mqtt = mqtt_client.Client(client_id)
mqtt.username_pw_set(username, password)
mqtt.connect(broker, port)
mqtt.loop_start()

def on_message(client, userdata, msg):
    global tty
    print("Message received-> " + msg.topic + " " + str(msg.payload))
    channel = int(msg.payload)
    send_channel(tty, channel)
mqtt.on_message = on_message

# setup number in ha
print(f"Setting up {client_id} ...")
payload = f'{{"unique_id": "{client_id}", "name": "{client_id}", "command_topic": "homeassistant/number/{client_id}/set", "state_topic": "homeassistant/switch/{client_id}/state", "min": 1, "max": 4}}'
mqtt.publish(f"homeassistant/number/{client_id}/config", payload=payload, retain=True)
mqtt.publish(f"homeassistant/number/{client_id}/state", 0)
mqtt.subscribe(f"homeassistant/number/{client_id}/set")

def recv_channel(tty: serial.Serial, data: bytes):
    channel: Optional[int] = None
    if tty.in_waiting:
        data += tty.read_all()
        print(data)
        found = re.findall(b"G0[0-4]gA", data)
        #print(found)
        data = data[-12:]

        if found:
            try:
                channel = int(found[-1][1:3])
                #print(channel)
            except Exception as e:
                print(e)
                return None
            assert 1 <= channel <= 4
    return channel

def send_channel(tty: serial.Serial, channel: int) -> None:
    assert 1 <= channel <= 4
    print(f"Setting channel to {channel}")
    cmd = "G0{port}gA".format(port=channel).encode()
    print(f"Sending via serial: {cmd}")
    tty.write(cmd)
    tty.flush()

buffer = b''
current_channel = -1
while True:
    try:
        if tty is None:
            tty = serial.Serial(com, 19200)
            print(f"Reconnecting to {com} ...")
        else:
            channel = recv_channel(tty, buffer)
            if channel is not None and channel != current_channel:
                print(f"Recv Channel via Serial: {channel}")
                if current_channel != channel:
                    print(f"Publishing {client_id} state {channel} via mqtt")
                    mqtt.publish(f"homeassistant/number/{client_id}/state", channel)
                    current_channel = channel
    except:
        if tty is not None:
            tty.close()
            tty = None
            print("Disconnecting")

        print("No Connection")
        time.sleep(2)
            

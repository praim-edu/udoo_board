import paho.mqtt.client as mqtt
import pickle
import datetime
import wave
import sys, os, django
sys.path.append("C:/Users/matti/Documents/corsopraim/django/audiotrappola") #here store is root folder(means parent).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "audiotrappola.settings")
django.setup()
from server import models
from django.utils import timezone

import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('broker')
args = parser.parse_args()
BROKER=args.broker


class AudioMessage:
    def __init__(self, type):
        self.msg_type = type
        self.audio = ""
        self.level = 0.0


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    
nomeFile = ""
registra = False
buffer = ""
starts = timezone.now()

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global registra
    global nomeFile
    global buffer
    global starts
    m = pickle.loads(msg.payload)
    #print "message arrived " + str(m)

    if m.msg_type == 0:
        registra = True
        buffer = ""
        nomeFile = timezone.now().strftime("%Y%m%d%H%M%S") + ".wav"
        starts = timezone.now()

    if registra:
        buffer = buffer + m.audio

    if m.msg_type == 2 and registra:
        print nomeFile
        f = wave.open("audiotrappola/server/static/server/" + nomeFile,'wb')
        f.setnchannels(1)
        f.setframerate(44100)
        f.setsampwidth(2)
        f.writeframes(buffer)
        f.close()
        registra = False
        a = models.SoundTrack()
        a.starts_at = starts
        a.ends_at = timezone.now()
        a.file_name = nomeFile
        a.max_volume = m.level
        a.min_volume = 10
        a.save()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print("receiver attempting connection")
client.connect(BROKER, 1883, 60)
client.subscribe("/signal")
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

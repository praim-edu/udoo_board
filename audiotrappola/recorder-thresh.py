#!/usr/bin/env python

from __future__ import print_function

import paho.mqtt.client as mqtt
import sys
import time
import getopt
import alsaaudio
import pickle
import numpy as np

def usage():
    print('usage: recorder.py [-d <device>] [-h <host>] [-l <level>]', file=sys.stderr)
    print('    use <level> between -70 and 0', file=sys.stderr)
    sys.exit(2)

class AudioMessage:
    def __init__(self, type):
        self.msg_type = type
        self.audio = ""

def getlevel(data):
    y = np.fromstring(data, dtype=np.int16).astype(np.int32)
    m = np.mean(y**2)
    rms = np.sqrt(m)
    return 20 * np.log10(rms/(2**15))

def waitaudio(source, level):
    while True:
        l, data = source.read()
        if l:
            x = getlevel(data)
            if x > level:
                print('found level: ', x, ' > ', level)
                return data

# inp, level, client, data)
def sendaudio(source, level, client, data):
    mtype = 0
    starttime = time.time()
    while True:
        if mtype == 1 and time.time() - starttime > 2:
            mtype = 2
        msg = AudioMessage(mtype)
        msg.audio = data
        client.publish('/signal',pickle.dumps(msg, 2))
        if mtype == 2:
            print ('end audio segment')
            return
        elif mtype == 0:
            mtype = 1

        l, data = source.read()
        if l and getlevel(data) > level:
            starttime = time.time()

if __name__ == '__main__':

    device = 'default'
    host = 'localhost'
    level = -55.0

    opts, args = getopt.getopt(sys.argv[1:], 'd:h:l:')
    for o, a in opts:
        if o == '-d':
            device = a
            print("Device is: "+device)
        if o == '-h':
            host = a
            print("Host is: "+host)
        if o == '-l':
            level = float(a)
            print ("Threshold level is ", level, " db")

    print("Other args:", str(args))
    # print str(args)
    if args:
        usage()

    client = mqtt.Client()
    client.connect(host, 1883, 60)

    # Open the device in nonblocking capture mode. The last argument could
    # just as well have been zero for blocking mode. Then we could have
    # left out the sleep call in the bottom of the loop
    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, device=device)

    # Set attributes: Mono, 44100 Hz, 16 bit little endian samples
    inp.setchannels(1)
    inp.setrate(44100)
    inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

    # The period size controls the internal number of frames per period.
    # The significance of this parameter is documented in the ALSA api.
    # For our purposes, it is suficcient to know that reads from the device
    # will return this many frames. Each frame being 2 bytes long.
    # This means that the reads below will return either 320 bytes of data
    # or 0 bytes of data. The latter is possible because we are in nonblocking
    # mode.
    inp.setperiodsize(160)
    
    client.loop_start()

    # loops = 500
    while True:
        data = waitaudio(inp, level)
        # Read data from device
        sendaudio(inp, level, client, data)

    client.loop_stop()


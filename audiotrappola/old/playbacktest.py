#!/usr/bin/env python

## playbacktest.py
##
## This is an example of a simple sound playback script.
##
## The script opens an ALSA pcm for sound playback. Set
## various attributes of the device. It then reads data
## from stdin and writes it to the device.
##
## To test it out do the following:
## python recordtest.py out.raw # talk to the microphone
## python playbacktest.py out.raw


from __future__ import print_function

import sys
import time
import getopt
import alsaaudio
import numpy

def usage():
    print('usage: playbacktest.py [-d <device>] <file>', file=sys.stderr)
    sys.exit(2)

if __name__ == '__main__':

    device = 'default'
    level = -60.0

    opts, args = getopt.getopt(sys.argv[1:], 'd:l:')
    for o, a in opts:
        if o == '-d':
            device = a
        if o == '-l':
            level = float(a)

    if not args:
        usage()

    f = open(args[0], 'rb')

    # Open the device in playback mode. 
    out = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK, device=device)

    # Set attributes: Mono, 44100 Hz, 16 bit little endian frames
    out.setchannels(1)
    out.setrate(44100)
    out.setformat(alsaaudio.PCM_FORMAT_S16_LE)

    # The period size controls the internal number of frames per period.
    # The significance of this parameter is documented in the ALSA api.
    out.setperiodsize(160)

    # Read data from stdin
    data = f.read(440)
    #y = numpy.fromstring(data, dtype=numpy.int16).astype(numpy.int32)
    #m = numpy.mean(y**2)
    #print('vector ', y)
    #print('squared ', y**2)
    #print('mean ', m)
   
    while data:
        y = numpy.fromstring(data, dtype=numpy.int16).astype(numpy.int32)
        m = numpy.mean(y**2)
        if m < 0:
            print('mean ', m)
            print('vector ', y)
            print('squared ', y**2)
        else:
            rms = numpy.sqrt(m)

            # Take the logarithmic value
            db = 20 * numpy.log10(rms/(2**15))
            if (db > level):
                print('decibel ', db, ' mean: ', m, ' rms: ', rms, ' ratio: ', (2**15), ' > ', rms/(2**15))

        out.write(data)
        data = f.read(440)

        

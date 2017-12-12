#!/bin/bash

#mosquitto &
#PID_1="$!"

#BROKER="10.2.2.200"

BROKER="$1"

python audiotrappola/recorder-thresh.py -h "$BROKER" -d plughw:CARD=Beecaster,DEV=0 -l -45 &
PID_2="$!"

pushd django/audiotrappola/
python receiver.py "$BROKER" &
PID_3="$!"
popd

pushd django/audiotrappola
python manage.py runserver 0.0.0.0:8000 &
PID_4="$!"
popd


read -p "press a key to exit"


#kill -9 "$PID_1"
kill -9 "$PID_2"
kill -9 "$PID_3"
kill -9 "$PID_4"
 

 

killall python


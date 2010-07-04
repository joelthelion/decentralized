#!/bin/bash
terminate () {
    kill $(jobs -p)
    exit
    }

trap "terminate" SIGINT
./wsgi_ui.py&
while :
do
    ./rsslinks.py &&
    ./update_predictions.py &
    sleep 1000
done

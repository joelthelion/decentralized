#!/bin/bash
./wsgi_ui.py&
while :
do
    ./rsslinks.py
    ./update_predictions.py
    sleep 1000
done

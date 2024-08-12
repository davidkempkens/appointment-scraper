#!/bin/bash

# source scraping-env/Scripts/activate

# run duesseldorf.py every minute
while true; do
    python run.py
    sleep 60
done

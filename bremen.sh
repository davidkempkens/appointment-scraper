#!/bin/bash

source venv/Scripts/activate

while true; do
    python run.py Bremen &
    sleep 60
done

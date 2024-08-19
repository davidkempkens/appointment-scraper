#!/bin/bash

source venv/Scripts/activate

while true; do
    python run.py Duesseldorf &
    sleep 60
done

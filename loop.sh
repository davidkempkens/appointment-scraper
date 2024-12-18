#!/bin/bash

# linux
source venv/bin/activate

# first argument is the city name
city=$1

# second argument is the concern
concern=$2

# check if the city name is provided
if [ -z "$city" ]; then
    echo "Please provide the city name as the first argument"
    exit 1
fi

# check if the concern is provided
if [ -z "$concern" ]; then
    echo "Please provide the concern as the second argument"
    exit 1
fi

# main loop
while true; do
    python main.py "$city" "$concern"
    sleep 60
done

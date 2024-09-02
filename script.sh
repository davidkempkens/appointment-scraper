#!/bin/bash

source venv/Scripts/activate

# first argumtent is the city name
city=$1

# check if the city name is provided
if [ -z "$city" ]; then
    echo "Please provide the city name as the first argument"
    exit 1
fi

echo "City: $city"

while true; do
    python run.py $city
    sleep 60
done

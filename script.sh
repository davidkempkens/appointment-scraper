#!/bin/bash

# windows
# source venv/Scripts/activate

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
    echo "When no area is provided, the default area is \"personalausweis_antrag\""
    concern="personalausweis_antrag"
fi

# sleep time in seconds
sleep_time=60

# run the script
echo "$city $concern $sleep_time"

while true; do
    if [ "$city" == "dresden" ]; then
        python run.py "$city" "$concern" & 
        sleep 240
    else
        python run.py "$city" "$concern"
    fi
    sleep $sleep_time
done

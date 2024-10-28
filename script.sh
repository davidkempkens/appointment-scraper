#!/bin/bash

# windows
# source venv/Scripts/activate

# linux
source venv/bin/activate

# first argument is the city name
city=$1

# second argument is the concern
concern=$2

sleep_time=$3

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
if [ -z "$sleep_time" ]; then
    sleep_time=60
else
    sleep_time=$((sleep_time))
    echo "Sleep time is $sleep_time seconds"
fi

# run the script
# echo "$city $concern $sleep_time"

while true; do
    python run.py "$city" "$concern"
    sleep $sleep_time
done

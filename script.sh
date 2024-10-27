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

echo "City: $city"
echo "Concern: $concern"

while true; do
    python run.py "$city" "$concern"
    sleep 60
done

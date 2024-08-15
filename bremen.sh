#!/bin/bash

# if conda environment is not activated, activate it
# conda activate scraping

while true; do
    python run.py Bremen &
    sleep 60
done

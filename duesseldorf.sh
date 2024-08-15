#!/bin/bash

# if conda environment is not activated, activate it
# conda activate scraping

while true; do
    python run.py Duesseldorf &
    sleep 60
done

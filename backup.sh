#!/bin/bash

# check if the backup folder exists
if [ ! -d backup ]; then
    mkdir backup
fi

echo "Backup at $(date +%Y-%m-%d_%H-%M-%S)"

# copy the database to the backup folder
cp database.db backup/database_$(date +%Y-%m-%d_%H-%M-%S).db

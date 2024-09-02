#!/bin/bash

# check if the backup folder exists
if [ ! -d db/backup ]; then
    mkdir db/backup
fi

echo "Backup at $(date +%Y-%m-%d_%H-%M-%S)"

# copy the database to the backup folder
cp db/database.db db/backup/database_$(date +%Y-%m-%d_%H-%M-%S).db

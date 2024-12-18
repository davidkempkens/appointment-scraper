#!/bin/bash

# check if the backup folder exists
if [ ! -d db/backup ]; then
    mkdir db/backup
fi

echo "Backup at $(date +%Y-%m-%d_%H-%M-%S)"

cp db/duesseldorf.db db/backup/duesseldorf_$(date +%Y-%m-%d_%H-%M-%S).db
cp db/dresden.db db/backup/dresden_$(date +%Y-%m-%d_%H-%M-%S).db
cp db/kiel.db db/backup/kiel_$(date +%Y-%m-%d_%H-%M-%S).db

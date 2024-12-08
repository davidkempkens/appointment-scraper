#!/bin/bash

if [ -f .env ]; then
    export $(cat .env | xargs)
else
    echo "No .env file found"
    exit 1
fi

SERVER=$SERVER

if [ -z "$SERVER" ]; then
    echo "No SERVER found in .env file"
    exit 1
fi

USER=$USER
if [ -z "$USER" ]; then
    echo "No USER found in .env file"
    exit 1
fi

REMOTE_PATH=$REMOTE_PATH
if [ -z "$REMOTE_PATH" ]; then
    echo "No REMOTE_PATH found in .env file"
    exit 1
fi

rsync -avz $USER@$SERVER:$REMOTE_PATH/dresden.db ./db
rsync -avz $USER@$SERVER:$REMOTE_PATH/duesseldorf.db ./db
rsync -avz $USER@$SERVER:$REMOTE_PATH/kiel.db ./db

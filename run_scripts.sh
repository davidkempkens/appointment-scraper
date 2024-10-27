#!/bin/bash

# Start a new tmux session
SESSION="mysession"
tmux new-session -d -s $SESSION

# Liste von Argumenten, die an das Skript übergeben werden
args=("debug" "debug" "debug")

for i in "${!args[@]}"; do
  if [ "$i" -eq 0 ]; then
    # Erster Befehl in der initialen tmux-Fenster
    tmux send-keys -t $SESSION "./script.sh ${args[$i]}" C-m
  else
    # Neues Panel für jeden weiteren Befehl
    tmux split-window -t $SESSION
    tmux select-layout -t $SESSION tiled
    tmux send-keys -t $SESSION "./script.sh ${args[$i]}" C-m
  fi
done

# Sitzung anhängen
tmux attach -t $SESSION

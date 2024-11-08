#!/bin/bash

# Start a new tmux session for a city
# the first argument is the city name



CITY=$1
SESSION="${CITY}"
CONCERNS=("anmeldung" "ummeldung" "abmeldung" "personalausweis_antrag" "reisepass_antrag")

tmux new-session -d -s $SESSION

if [ $SESSION = "dash" ]; then
  tmux send-keys -t $SESSION "source venv/bin/activate" C-m
  tmux send-keys -t $SESSION "python app_v2.py" C-m
else
  for i in "${!CONCERNS[@]}"; do
    if [ "$i" -eq 0 ]; then
      # Erster Befehl in der initialen tmux-Fenster
      tmux send-keys -t $SESSION "./script.sh ${CITY} ${CONCERNS[$i]}" C-m
    else
      # Neues Panel für jeden weiteren Befehl
      tmux split-window -t $SESSION
      tmux select-layout -t $SESSION even-vertical
      tmux send-keys -t $SESSION "./script.sh ${CITY} ${CONCERNS[$i]}" C-m
    fi
  done
fi

# Sitzung anhängen
tmux attach -t $SESSION

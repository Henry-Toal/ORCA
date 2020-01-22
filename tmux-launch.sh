#!/bin/bash
# usage: add this to crontab:
# @reboot /home/pi/ORCA/tmux-launch.sh

SESSION_NAME=orca

tmux list-sessions | grep $SESSION_NAME > /dev/null 2>&1
if [ $? -eq 0 ]; then
	echo "session already started"
	echo "use: tmux attach -t $SESSION_NAME:launcher"
	echo "---"
	echo "attaching you to that session in 3 seconds"
	for I in 1 2 3 4; do
		echo -n "."
		sleep 1
	done
	tmux attach -t $SESSION_NAME:launcher
	exit 1
fi

tmux new-session -d -s $SESSION_NAME -n launcher
tmux send-keys -t $SESSION_NAME:launcher "$(dirname ${0})/launch.sh" Enter
echo "attach to tmux with: tmux attach -t $SESSION_NAME:launcher"

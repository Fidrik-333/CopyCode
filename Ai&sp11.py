#!/bin/bash

echo "=== Linux System Health Expert ==="
echo "Describe your system issue:"
echo "1) High CPU usage"
echo "2) Low disk space"
echo "3) Network not working"
echo "4) Exit"

read -p "Enter the option number: " choice

if [ "$choice" == "1" ]; then
    echo "Recommendation: Check top processes using:"
    echo "Command: top -o %CPU | head -n 12"
    echo "Suggestion: Kill unnecessary processes, restart services if needed."

elif [ "$choice" == "2" ]; then
    echo "Recommendation: Check disk usage with:"
    echo "Command: df -h"
    echo "Suggestion: Clean temp files (sudo rm -rf /tmp/*), remove old log files."

elif [ "$choice" == "3" ]; then
    echo "Recommendation: Test connectivity using:"
    echo "Command: ping -c 4 8.8.8.8"
    echo "Suggestion: Restart network service (sudo systemctl restart NetworkManager), check cables."

elif [ "$choice" == "4" ]; then
    echo "Exiting. Have a healthy system!"

else
    echo "Invalid option. Please try again."
fi

#!/bin/bash

# Run usage_manager.py in the background
python3 'usage_manager.py' 'add' &
python3 'usage_manager.py' 'update' &
sleep "10"

# Get the number of lines in the file
absolute_path=$(realpath "$0")
# go back one folder
base_path=$(dirname "$absolute_path")
base_path=$(dirname "$base_path")
echo "base_path: $base_path"

mail_file="$base_path/assets/fresh_outlook_mails.txt"
proxy_file="$base_path/assets/fresh_proxies.txt"
mails=$(wc -l < "$mail_file")
proxies=$(wc -l < "$proxy_file")
echo "-- There are $mails mails in $mail_file"
echo "-- There are $proxies proxies in $proxy_file"

if ((proxies < mails)); then
    echo "There are less proxies than mails. Please add more proxies."
    exit 1
fi



# Prompt the user for input
read -p "Enter total number of bots: " x
read -p "Enter number of bots per batch: " batchSize
read -p "Enter delay in seconds: " delay

# Loop through the range of numbers and run account_creator.py
jobs=()
for ((i = 0; i < x; i += batchSize)); do
    for ((j = i; j < i + batchSize && j <= x; j++)); do
        python3 "account_creator.py" "$j" "$batchSize" &
        jobs+=($!)
    done
    for job in "${jobs[@]}"; do
        wait "$job"
    done
    jobs=()
    if ((i + batchSize < x)); then
        echo "Waiting for $delay seconds before next batch..."
        sleep "$delay"
    fi
done
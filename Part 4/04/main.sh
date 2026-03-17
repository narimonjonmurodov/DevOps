#!/bin/bash
source "$(dirname $0)/config.conf"
source "$(dirname $0)/check.sh"

CHECK $@ || exit 1

for day in {1..5}; do
    logfile="$(dirname $0)/nginx_log_day${day}.log"
    echo "Generating $logfile..."
    entries=$((RANDOM % 901 + 100))
    start_ts=$(date -d "2026-03-0${day} 00:00:00" +%s)
    end_ts=$(date -d "2026-03-0${day} 23:59:59" +%s)

    last_time=$start_ts

    for ((i=1; i<=entries; i++)); do
        ip="$((RANDOM%256)).$((RANDOM%256)).$((RANDOM%256)).$((RANDOM%254 + 1))"

        rand_sec=$((RANDOM%(end_ts - last_time + 1)))
        ts=$((last_time + rand_sec))
        last_time=$ts
        date_str=$(date -d "@$ts" "+%d/%b/%Y:%H:%M:%S +0500")

        method=${methods[RANDOM % ${#methods[@]}]}
        url=${urls[RANDOM % ${#urls[@]}]}
        code=${codes[RANDOM % ${#codes[@]}]}
        bytes=$((RANDOM%4901 + 100))
        agent=${agents[RANDOM % ${#agents[@]}]}

        echo "$ip - - [$date_str] \"$method $url HTTP/1.1\" $code $bytes \"-\" \"$agent\"" >> $logfile
    done
done

echo "Done generating 5 nginx log files!"

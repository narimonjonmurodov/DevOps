#!/bin/bash
start_time=$(date +"%Y-%m-%d %H:%M:%S")
start_ts=$(date +%s)

source "$(dirname $0)/check.sh"
source "$(dirname $0)/create_log.sh"
source "$(dirname $0)/data.sh"

CHECK $@ || exit 1
log_file=$( LOG ) || exit 1
DATA $@ $log_file || exit 1

end_time=$(date  +"%Y-%m-%d %H:%M:%S")
end_ts=$(date +%s)

duration=$(( end_ts - start_ts ))
hours=$(( duration / 3600 ))
minutes=$(( (duration % 3600) / 60 ))
seconds=$(( duration % 60 ))
total_time=$(printf "%02d:%02d:%02d" $hours $minutes $seconds)

echo "Start time: $start_time"
echo "End time: $end_time"
echo "Total running time: $total_time"
echo "Total running time in seconds: $duration"

echo "Start time: $start_time" >> $log_file
echo "End time: $end_time" >> $log_file
echo "Total running time: $total_time" >> $log_file
echo "Total running time in seconds: $duration" >> $log_file

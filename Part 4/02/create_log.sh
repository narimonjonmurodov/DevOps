#!/bin/bash

LOG_CHECK() {
path=$(dirname "$0")
count=$(ls -l "$path"/*.log 2>/dev/null | wc -l )
if [ "$count" -gt 1 ]
then
  echo "Error: you have more than 1 logfiles in $path/ " >&2
  echo "Please delate not related logfiles !" >&2
  return 1
elif [ $count -eq 1 ]
then
  file=$(ls "$path"/*.log)
else
  file="$path/$1"
  echo "full_path       creation_date       file_size" > "$file"
fi

echo $file
}

LOG() {
file="$(date +%d.%m.%Y_%H-%M-%S).log"
log_file=$(LOG_CHECK $file) || return 1

echo $log_file
}


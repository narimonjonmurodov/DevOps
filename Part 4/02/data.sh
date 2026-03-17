#!/bin/bash
source "$(dirname $0)/functions1.sh"
source "$(dirname $0)/functions2.sh"
source "$(dirname $0)/functions3.sh"
source "$(dirname $0)/functions4.sh"

DATA() {
log_file=${!#}
choice="/home/narimon/ /home/ /tmp/ /var/tmp/ /opt/ /srv/ /mnt/ /media/"
ALLOWED $choice
if [[ -z ${list[1]} ]]
then
  echo "I have no permission to do this!"
  return 1
fi

while true
do
  base=${list[$((RANDOM % ${#list[@]}))]}
  FILE_COUNTER $base
  if [ $count_files -le 100 ]
  then
     folder=$(NAMING $base 1 $1)
  else
     folder=$default_folders
  fi
  files=$(FILE_NAMING $folder $2 10)
  CREATING_DIR $folder $log_file
  CREATING_FILE $files $3 $log_file || return 0
done
}

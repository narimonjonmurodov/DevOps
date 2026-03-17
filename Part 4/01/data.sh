#!/bin/bash
source "$(dirname $0)/create_log.sh"
source "$(dirname $0)/functions1.sh"
source "$(dirname $0)/functions2.sh"
source "$(dirname $0)/functions3.sh"

DATA() {
log_file=$(LOG)

if ! [ ${1: -1} = "/" ]
then
  path="$1/"
else
  path=$1
fi

for (( i=0; i<$2; i++ ))
do
  folder=$(NAMING $path 1 $3)
  files=$(FILE_NAMING $folder $5 $4)
  CREATING_DIR $folder $log_file
  CREATING_FILE $files $6 $log_file || return 1
done

}

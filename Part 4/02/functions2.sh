#!/bin/bash
source "$(dirname $0)/functions1.sh"

FILE_NAMING(){
# 1st_list=paths last_2nd=name_extension last=emount
emount=${!#}
l_second=$(( $# - 1 ))
name=$(echo ${!l_second} | cut -d '.' -f1 )
extension=".$(echo ${!l_second} | cut -d '.' -f2)"
file_names=""

while [ $# -gt 2 ]
do
  file_names+="$(NAMING $1/ $emount $name $extension) "
  shift
done
echo $file_names
}

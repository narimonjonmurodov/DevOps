#!/bin/bash

STRING_REP() {
str=""
for ((i=0; i<$2; i++)); do
  str+="$1"
done
echo $str
}

NAMING() {
# 1st=absolute_path, 2nd=emount, 3rd=name, 4th=extension
date=$(date +%d%m%y)
names=""
name=$3
if [ ${#3} -lt 4 ]
then
  n=$(( 4 - ${#3} ))
else
  n=0
fi
count=$2

for ((i=0; i<count; i++)); do
  if (( i % 2 == 0 )); then
    name="$1$(STRING_REP ${3::1} $n)$3_$date$4"
  else
    name="$1$3$(STRING_REP ${3: -1} $n)_$date$4"
  fi
  n=$(( $n + 1 ))
  if [ -e $name ]
  then
    count=$(($count+1))
  else
    names+="$name "
  fi
done
echo $names
}

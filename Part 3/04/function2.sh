#!/bin/bash

ip_and_mask() {
IP=$(hostname -I | awk '{print $1}')
IP_MASK=$(ip -4 a | grep "$IP" | awk '{print $2}')
echo "$IP_MASK"
}

prefix_to_mask() {
MASK=""
REMAIN=$1
for i in 1 2 3 4
do
  if [ $REMAIN -ge 8 ]
  then
  MASK+="255"
  REMAIN=$(($REMAIN - 8))
  else
  MASK+=$((256 - 2**(8 - REMAIN)))
  REMAIN=0
  fi
  if [ $i -ne 4 ]
  then
  MASK+="."
  fi
done
echo "MASK = $MASK"
}

IP() {
echo "IP = $(ip_and_mask | cut -d'/' -f1)"
}

MASK() {
mask=$(ip_and_mask | cut -d'/' -f2)
prefix_to_mask $mask
}

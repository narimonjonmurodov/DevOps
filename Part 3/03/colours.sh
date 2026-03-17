#!/bin/bash


COLOUR() {
c_code=40;
colour="\033["
while [ -n "$1" ]
do
case $1 in
  1) base=7 ;;  # white
  2) base=1 ;;  # red
  3) base=2 ;;  # green
  4) base=4 ;;  # blue
  5) base=5 ;;  # purple
  6) base=0 ;;  # black
esac
colour+=$(($c_code+$base))
c_code=30
if [ $# -eq 2 ]
then
colour+=";"
fi
shift
done
echo $colour
}

PRINT() {
reset="\033[0m"
coulmn1=$(COLOUR $1 $2)
coulmn2=$(COLOUR $3 $4)
c1=$(echo $5 | awk -F= '{print $1}')
c2=$(echo $5 | awk -F= '{print $2}')
echo -e "${coulmn1}m${c1}${reset} = ${coulmn2}m${c2}${reset}"
}

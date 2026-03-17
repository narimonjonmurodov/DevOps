#!/bin/bash

source "$(dirname $0)/colours.sh"
source "$(dirname $0)/checking_input.sh"
source "$(dirname $0)/data.sh"
source "$(dirname $0)/table.sh"
source "$(dirname $0)/config.conf"

if [ $# -ne 0 ]
then
echo "The script runs without parameters !"
echo "The parameters are set in the config.conf file before the script is running"
exit 1
fi

parametrs="$column1_background $column1_font_color $column2_background $column2_font_color"

CHECK $parametrs
default=$?

if [ $default -eq 2 ]
then
parametrs="1 2 1 6"
flag="1"
elif [ $default -eq 1 ]
then
exit 1
fi

DATA | while IFS= read -r line
do
  PRINT $parametrs "$line"
done

TABLE $parametrs $flag

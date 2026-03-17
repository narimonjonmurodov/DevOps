#!/bin/bash

CHECK() {
dir="$(dirname $0)/"

if [ $# -ne 0 ]
then
   echo "Error: Script runs withouth Parametrs"
   return 1
elif compgen -G $dir"nginx_log_day[1-5].log" > /dev/null; then
   echo "Error: nginx log files already exist!"
   echo "If you want run this code please delete files first for not to get crash!"
   return 1
fi
}

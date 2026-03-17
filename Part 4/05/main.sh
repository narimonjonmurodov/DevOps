#!/bin/bash
source "$(dirname $0)/check.sh"

CHECK $@ || exit 0
CHECK_LOGS || exit 0
path="$(dirname $0)/../04/"

case $1 in
  1)
     awk '{print $0}' ${path}nginx_log_day*.log | sort -k9
  ;;

  2)
     awk '!ip[$1]++ {print $1}' ${path}nginx_log_day*.log | sort
  ;;

  3)
     awk '$9 >= 400 && $9 < 600' ${path}nginx_log_day*.log | sort
  ;;

  4)
     awk '$9 >= 400 && $9 < 600 && !ip[$1]++ {print $1}' ${path}nginx_log_day*.log | sort
  ;;

  *)
     echo "Error(1st parametr): Invalid parameter. Use 1, 2, 3 or 4 !"
     exit 1
  ;;
esac

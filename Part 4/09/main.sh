#!/bin/bash
source "$(dirname $0)/metrics.sh"
source "$(dirname $0)/functions.sh"
source "$(dirname $0)/check_sudo.sh"

if [ $# -ne 1 ]
then
   echo "Error: Script runs with 1 parametr"
   echo "Please run ./main --help for extra info"
   exit 1
fi

case "$1" in

--start)
CHECK_SUDO || exit 1
check_requirements || exit 1
status 2>/dev/null || exit 1
METRICS &
echo $! > "$(dirname $0)/exporter.pid"
echo "Exporter started with PID $!"
;;

--stop)
CHECK_SUDO || exit 1
stop
;;

--status)
status
;;

--help)
cat "$(dirname $0)/README.txt"
;;

*)
echo "Invalid option. Run ./main --help for extra info"
;;
esac

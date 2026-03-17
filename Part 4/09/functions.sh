#!/bin/bash
dir_exist() {
if [ ! -f "$(dirname $0)/exporter.pid" ]; then
    echo "Exporter is NOT running." 1>&2
    return 1
fi
echo $(cat exporter.pid)
}

check_requirements() {
if ! command -v nginx &> /dev/null
then
    echo "NGINX is not installed!"
    return 1
fi
if [ ! -d "$OUTPUT_DIR" ]; then
    sudo mkdir -p $OUTPUT_DIR
fi
}

stop() {
PID=$(dir_exist) || return 1

kill $PID 2>/dev/null
rm $(dirname $0)/exporter.pid
echo "Exporter stopped."
}

status() {
PID=$(dir_exist) || return 0

if ps -p $PID > /dev/null
then
    echo "Exporter running with PID $PID"
    return 1
else
    echo "Exporter is NOT running." 1>&2
fi
}


#!/bin/bash

# prinring hostname
function HOSTNAME {
echo "HOSTNAME = $(hostname)"
}

# printing timezone
TIMEZONE() {
TZ_name=$(cat /etc/timezone)
utc="UTC $(date +%:z | cut -d: -f1)"
echo "TIMEZONE = $TZ_name $utc"
}

#Current user who runs script
USER() {
user_name=$(whoami)
echo "USER = $user_name"
}

OS() {
OS=$(cat /etc/issue | cut -d'\' -f1)
echo "OS = $OS"
}

DATE() {
echo "DATE = $(date +"%d %B %Y %T")"
}

UPTIME() {
echo "UPTIME = $(uptime -p | cut -d' ' -f2,3)"
}

UPTIME_SEC(){
echo "UPTIME_SEC = $(cat /proc/uptime | cut -d' ' -f1)"
}


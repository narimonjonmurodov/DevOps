#!/bin/bash
path=$(dirname $0)
LOG_FILES="${path}/../04/nginx_log_day*.log"
REPORT=="${path}/report.html"
PORT=7890

terminal_analysis() {
echo "Starting GoAccess terminal dashboard..."
goaccess $LOG_FILES --log-format=COMBINED
}

web_interface() {
SERVER_IP=$(hostname -I | awk '{print $1}')
echo "Starting GoAccess dashboard..."
goaccess $LOG_FILES \
--log-format=COMBINED \
--real-time-html \
--ws-url=ws://$SERVER_IP:7890 \
-o report.html &
echo
echo "Open this in your browser:"
echo "http://$SERVER_IP:8080/report.html"
echo

python3 -m http.server 8080
echo
echo "Server is closed"
}

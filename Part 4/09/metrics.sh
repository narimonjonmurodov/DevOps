#!/bin/bash
OUTPUT_DIR="/var/www/metrics"
OUTPUT="/var/www/metrics/metrics.html"

METRICS() {

while true
do

CPU_idle=$(top -bn1 | grep "Cpu(s)" | awk -F, '{print $4}')
CPU_USED=$(echo $CPU_idle | awk '{print 100 - $1}')
RAM_USED=$(free -m | awk '/^Mem:/ {print $3}')
RAM_AVAILABLE=$(free -m | awk '/^Mem:/ {print $7}')
DISK_FREE=$(df -k / | awk 'NR==2 {print $4}')

cat <<EOF > $OUTPUT
# HELP cpu_usage CPU usage percentage
# TYPE cpu_usage gauge
cpu_usage $CPU_USED

# HELP ram_used RAM used in MB
# TYPE ram_used gauge
ram_used $RAM_USED

# HELP ram_available RAM available in MB
# TYPE ram_available gauge
ram_available $RAM_AVAILABLE

# HELP disk_free Disk free space in KB
# TYPE disk_free gauge
disk_free $DISK_FREE
EOF

sleep 3

done
}

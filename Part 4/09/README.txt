# ==========================================
# Custom Node Exporter (Bash Version)
# Collects CPU, RAM, and Disk metrics
# Updates metrics every 3 seconds
# ==========================================
Usage:
  sudo ./main.sh --start      Start exporter
  sudo ./main.sh --stop       Stop exporter
  ./main.sh --status     Check exporter status
  ./main.sh --help     Show this help

Metrics collected:
  - CPU usage
  - RAM usage
  - Disk free space

Metrics endpoint:
  http://localhost/metrics/metrics.html

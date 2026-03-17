===================================================
Prometheus & Grafana Installation Script
===================================================

Description:
------------
This script installs Prometheus and Grafana on Ubuntu/Debian systems.
Prometheus collects system metrics, and Grafana visualizes them in dashboards.
Both services are configured to run automatically via systemd.

USAGE:
   ./main <OPTION>

OPTIONS:

   --help
   Shows this help message and usage instructions.

   --check
   Checks whether Prometheus, Node Exporter, and Grafana are installed and running on the system.

   1
   Install Prometheus.

   2
   Install Node Exporter.

   3
   Install Grafana.

   --all
   Install all monitoring components:
      Prometheus + Node Exporter + Grafana.
      
Accessing Web Interfaces:
-------------------------
Prometheus: http://<server-ip>:9090
Grafana:    http://<server-ip>:3000

Grafana default login:
Username: admin
Password: admin
(Change password on first login)

Adding Prometheus to Grafana:
-----------------------------
1. Log in to Grafana.
2. Go to Configuration → Data Sources → Add data source.
3. Select Prometheus.
4. Set URL to http://localhost:9090
5. Click Save & Test (should show "Data source is working")

Creating Dashboards:
-------------------
1. Click + → Dashboard → Add Panel.
2. Select Prometheus as data source.
3. Enter metric queries (e.g., node_cpu_seconds_total).
4. Add more panels as needed for RAM, disk, or network.
5. Save your dashboard.

Notes:
------
- Ensure ports 9090 (Prometheus) and 3000 (Grafana) are open in your firewall.
- Script works only on Ubuntu/Debian.
- Run script multiple times to install/update software.
- For support or issues, check Prometheus (https://prometheus.io/) and Grafana (https://grafana.com/) documentation.

===================================================

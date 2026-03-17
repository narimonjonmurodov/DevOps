#!/bin/bash

install_node_exporter() {
echo "Installing Node Exporter..."
cd /tmp || exit
wget -q https://github.com/prometheus/node_exporter/releases/download/v1.8.2/node_exporter-1.8.2.linux-amd64.tar.gz
tar -xzf node_exporter-1.8.2.linux-amd64.tar.gz
sudo cp node_exporter-1.8.2.linux-amd64/node_exporter /usr/local/bin/
sudo useradd -rs /bin/false node_exporter 2>/dev/null

sudo bash -c 'cat <<EOF > /etc/systemd/system/node_exporter.service
[Unit]
Description=Node Exporter
After=network.target

[Service]
User=node_exporter
Group=node_exporter
Type=simple
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=multi-user.target
EOF'

sudo systemctl daemon-reload
sudo systemctl enable node_exporter
sudo systemctl start node_exporter

echo "Node Exporter installed and started."
echo "Adding Node Exporter to Prometheus..."

if ! grep -q "node_exporter" /etc/prometheus/prometheus.yml; then

sudo bash -c 'cat <<EOF >> /etc/prometheus/prometheus.yml

  - job_name: "node_exporter"
    static_configs:
      - targets: ["localhost:9100"]
EOF'
fi

sudo systemctl restart prometheus
echo "Prometheus restarted."
echo "Installation completed!"
echo "Check metrics: http://localhost:9100/metrics"
echo "Check Prometheus targets: http://localhost:9090/targets"
}

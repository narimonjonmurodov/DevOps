#!/bin/bash

install_prometheus() {
echo "=== Installing Prometheus ==="
sudo useradd --no-create-home --shell /bin/false prometheus
PROM_VERSION="2.48.0"
wget https://github.com/prometheus/prometheus/releases/download/v${PROM_VERSION}/prometheus-${PROM_VERSION}.linux-amd64.tar.gz -O /tmp/prometheus.tar.gz
tar xvf /tmp/prometheus.tar.gz -C /tmp
cd /tmp/prometheus-${PROM_VERSION}.linux-amd64 || exit
sudo mv prometheus promtool /usr/local/bin/
sudo mkdir -p /etc/prometheus
sudo mv prometheus.yml /etc/prometheus/
sudo mkdir -p /var/lib/prometheus
sudo chown -R prometheus:prometheus /etc/prometheus /var/lib/prometheus
sudo bash -c 'cat <<EOF > /etc/systemd/system/prometheus.service
[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
Group=prometheus
Type=simple
ExecStart=/usr/local/bin/prometheus \
  --config.file /etc/prometheus/prometheus.yml \
  --storage.tsdb.path /var/lib/prometheus

[Install]
WantedBy=multi-user.target
EOF'

sudo systemctl daemon-reload
sudo systemctl enable prometheus
sudo systemctl start prometheus

echo "Prometheus installation completed! Access at: http://<server-ip>:9090"
}


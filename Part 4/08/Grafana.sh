#!/bin/bash

install_grafana() {
echo "=== Installing Grafana ==="

sudo apt update
sudo apt install -y software-properties-common wget apt-transport-https

sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
sudo apt update

sudo apt install grafana -y

sudo systemctl enable grafana-server
sudo systemctl start grafana-server

echo "Grafana installation completed! Access at: http://<server-ip>:3000 (default: admin/admin)"
}


#!/bin/bash
set -e

# Helper function for printing info
info() {
    echo "[*] $1"
}


echo "======================================"
echo "[*] Installing MicroK8s..."
echo "======================================"
sudo snap install microk8s --classic --channel=1.32/stable > /dev/null 2>&1

# Add current user to microk8s group for easier access
sudo usermod -aG microk8s $USER > /dev/null 2>&1
sudo chown -f -R $USER ~/.kube > /dev/null 2>&1

info "MicroK8s installed. You may need to log out and back in for permissions."

# --------------------------
# 2. Enable MicroK8s Addons
# --------------------------
info "Enabling MicroK8s addons (dns, storage, ingress)..."
sudo microk8s enable dns storage ingress > /dev/null 2>&1

# --------------------------
# 3. Verify Setup
# --------------------------
info "Verifying MicroK8s setup..."
sudo microk8s status --wait-ready > /dev/null 2>&1
info "MicroK8s setup complete."

sleep 2

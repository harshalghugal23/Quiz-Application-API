#!/bin/bash
set -e

NAMESPACE="quiz-api"
IMAGE_PATTERN="app:latest"
MYSQL_IMAGE="mysql:8"

echo "======================================"
echo "[*] Cleaning up Kubernetes resources"
echo "======================================"

# 1️⃣ Delete Deployments
echo "[*] Deleting backend deployment..."
sudo microk8s kubectl delete deployment quiz-backend -n $NAMESPACE --ignore-not-found

echo "[*] Deleting MySQL deployment..."
sudo microk8s kubectl delete deployment quiz-mysql -n $NAMESPACE --ignore-not-found

# 2️⃣ Delete Services
echo "[*] Deleting services..."
sudo microk8s kubectl delete svc quiz-backend -n $NAMESPACE --ignore-not-found
sudo microk8s kubectl delete svc quiz-mysql -n $NAMESPACE --ignore-not-found

# 3️⃣ Delete PersistentVolumeClaim
echo "[*] Deleting PVC..."
sudo microk8s kubectl delete pvc mysql-pvc -n $NAMESPACE --ignore-not-found

# 4️⃣ Delete Namespace
echo "[*] Deleting namespace..."
sudo microk8s kubectl delete namespace $NAMESPACE --ignore-not-found

# Wait a few seconds for resources to terminate
sleep 5

# 5️⃣ Remove images from MicroK8s containerd
echo "[*] Removing images..."
for img in $(sudo microk8s ctr images list | awk '{print $1}' | grep "$IMAGE_PATTERN"); do
    echo "[*] Removing image: $img"
    sudo microk8s ctr image remove "$img"
done
# 6️⃣ Optional: Stop and remove MicroK8s
echo "[*] Stopping MicroK8s..."
sudo microk8s stop

echo "[*] Uninstalling MicroK8s..."
sudo snap remove microk8s
sudo snap forget $(snap saved | tail -n 1 | awk '{print $1}')
cd ..
sudo rm -rf Quiz-Application-API
echo "======================================"
echo "[*] Cleanup completed!"
echo "======================================"

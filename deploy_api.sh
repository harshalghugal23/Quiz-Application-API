#!/bin/bash

# ------------------------------
# CONFIGURATION
# ------------------------------
source k8s/pull_img.sh
source k8s/setup_microk8s.sh

echo "======================================"
echo "[*] Initiating API deployment..."
echo "======================================"

BACKEND_IMAGE_TAR="k8s/quiz-backend.tar.gz"
BACKEND_IMAGE_NAME="localhost:32000/app:latest"
NAMESPACE="quiz-api"
MYSQL_YAML="k8s/mysql.yaml"
BACKEND_YAML="k8s/backend.yaml"

# NodePort ports
BACKEND_NODEPORT=30001
MYSQL_NODEPORT=33007  # Optional, usually not needed

# Wait settings
WAIT_INTERVAL=5   # seconds
WAIT_TIMEOUT=150  # seconds

# ------------------------------
# HELPER FUNCTIONS
# ------------------------------
log() { echo "[*] $1"; }
err() { echo "[!] $1"; }

wait_for_pod_ready() {
  local label=$1
  local elapsed=0
  log "Waiting for pods with label '$label' to be Ready..."
  while true; do
    ready=$(sudo microk8s kubectl get pods -n $NAMESPACE -l $label -o jsonpath='{.items[*].status.containerStatuses[*].ready}' | grep false || true)
    if [ -z "$ready" ]; then
      log "Pods with label '$label' are ready."
      break
    fi
    sleep $WAIT_INTERVAL
    elapsed=$((elapsed + WAIT_INTERVAL))
    if [ $elapsed -ge $WAIT_TIMEOUT ]; then
      err "Timeout waiting for pods with label '$label'."
      exit 1
    fi
  done
}

service_exists() {
  local svc=$1
  sudo microk8s kubectl get svc -n $NAMESPACE $svc &>/dev/null
}

# ------------------------------
# IMPORT BACKEND IMAGE INTO MICROK8S
# ------------------------------
if [ -f "$BACKEND_IMAGE_TAR" ]; then
  log "Importing backend image..."
  sudo gzip -dc "$BACKEND_IMAGE_TAR" | sudo microk8s ctr image import -
  IMAGE_ID=$(sudo microk8s ctr images list | grep app:latest | awk '{print $1}')
  if [ -n "$IMAGE_ID" ]; then
    sudo microk8s ctr images tag "$IMAGE_ID" "$BACKEND_IMAGE_NAME"
    sleep 2
    #sudo microk8s ctr images push "$BACKEND_IMAGE_NAME"
  else
    err "Backend image not found after import!"
    exit 1
  fi
else
  err "Backend image tar not found at '$BACKEND_IMAGE_TAR'. Skipping import."
fi

# ------------------------------
# CREATE NAMESPACE
# ------------------------------
log "Creating namespace '$NAMESPACE'..."
sudo microk8s kubectl create namespace $NAMESPACE 2>/dev/null || log "Namespace '$NAMESPACE' already exists."

# ------------------------------
# APPLY DEPLOYMENTS
# ------------------------------
log "Applying MySQL deployment..."
sudo microk8s kubectl apply -f $MYSQL_YAML -n $NAMESPACE

log "Applying backend deployment..."
sudo microk8s kubectl apply -f $BACKEND_YAML -n $NAMESPACE

# ------------------------------
# WAIT FOR PODS TO BE READY
# ------------------------------
wait_for_pod_ready "app=quiz-mysql"
wait_for_pod_ready "app=quiz-backend"

# ------------------------------
# EXPOSE SERVICES
# ------------------------------
if ! service_exists quiz-backend-nodeport; then
  log "Exposing backend via NodePort ($BACKEND_NODEPORT)..."
  sudo microk8s kubectl expose deployment quiz-backend \
    --type=NodePort \
    --name=quiz-backend-nodeport \
    --port=5001 \
    --target-port=5001 \
    --node-port=$BACKEND_NODEPORT -n $NAMESPACE
fi

if ! service_exists quiz-mysql-nodeport; then
  log "Optional: Exposing MySQL via NodePort ($MYSQL_NODEPORT)..."
  sudo microk8s kubectl expose deployment quiz-mysql \
    --type=NodePort \
    --name=quiz-mysql-nodeport \
    --port=3306 \
    --target-port=3306 \
    --node-port=$MYSQL_NODEPORT -n $NAMESPACE
fi

# ------------------------------
# PORT FORWARDING (fallback)
# ------------------------------
log "Forwarding Backend port 5001 to localhost..."
sudo microk8s kubectl port-forward svc/quiz-backend 5001:5001 -n $NAMESPACE &
BACKEND_FORWARD_PID=$!

log "Forwarding MySQL port 3306 to localhost..."
sudo microk8s kubectl port-forward svc/quiz-mysql 3306:3306 -n $NAMESPACE &
MYSQL_FORWARD_PID=$!

echo "======================================"                                                                                                   
echo "[*] API Deployed Successfully..."                                                                                                         
echo "======================================"

# ------------------------------
# ENDPOINTS
# ------------------------------
echo "===================================="
echo "Backend API Endpoints (Browser):"
echo "POST /api/register -> http://127.0.0.1:5001/api/register"
echo "POST /api/login    -> http://127.0.0.1:5001/api/login"
echo "MySQL available on localhost:3306 (for DB clients)"
echo "===================================="

# Keep script running to maintain port forwards
wait $BACKEND_FORWARD_PID $MYSQL_FORWARD_PID

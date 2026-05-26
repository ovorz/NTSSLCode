#!/usr/bin/env bash
# Installation script for the NTSSL artifact.
# This script prepares the Python environment and installs the dependencies
# required by the data processing, anomaly detection, semi-supervised learning,
# AS-level path analysis, and cross-layer analysis scripts.

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${PROJECT_ROOT}/.venv"
REQ_FILE="${PROJECT_ROOT}/requirements.txt"

echo "============================================================"
echo "[NTSSL Artifact] Installation started"
echo "Project root: ${PROJECT_ROOT}"
echo "============================================================"

# ------------------------------------------------------------
# 1. Check Python
# ------------------------------------------------------------
if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
else
    echo "[ERROR] python3 is not installed or not found in PATH."
    echo "Please install Python 3.8 or later and rerun this script."
    exit 1
fi

PYTHON_VERSION="$(${PYTHON_BIN} - <<'PY'
import sys
print(f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
PY
)"

echo "[INFO] Detected Python version: ${PYTHON_VERSION}"

${PYTHON_BIN} - <<'PY'
import sys
if sys.version_info < (3, 8):
    raise SystemExit("[ERROR] Python 3.8 or later is required.")
PY

# ------------------------------------------------------------
# 2. Optional system packages
# ------------------------------------------------------------
echo "[INFO] Checking optional system dependencies..."

if command -v apt-get >/dev/null 2>&1; then
    echo "[INFO] apt-get detected."

    if [ "${INSTALL_SYSTEM_DEPS:-0}" = "1" ]; then
        echo "[INFO] Installing optional system packages..."
        echo "[INFO] This may require sudo permission."

        sudo apt-get update
        sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
            python3-venv \
            python3-dev \
            build-essential \
            tcpdump \
            tshark \
            mysql-client

        echo "[INFO] Optional system packages installed."
    else
        echo "[INFO] Skipping system package installation."
        echo "[INFO] To install optional packages, run:"
        echo "       INSTALL_SYSTEM_DEPS=1 bash install.sh"
        echo "[INFO] Optional tools include tcpdump, tshark, and mysql-client."
    fi
else
    echo "[INFO] apt-get not found. Skipping system package installation."
fi

# ------------------------------------------------------------
# 3. Create virtual environment
# ------------------------------------------------------------
if [ ! -d "${VENV_DIR}" ]; then
    echo "[INFO] Creating virtual environment at ${VENV_DIR} ..."
    ${PYTHON_BIN} -m venv "${VENV_DIR}"
else
    echo "[INFO] Virtual environment already exists at ${VENV_DIR}."
fi

# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"

echo "[INFO] Upgrading pip, setuptools, and wheel..."
python -m pip install --upgrade pip setuptools wheel

# ------------------------------------------------------------
# 4. Generate requirements.txt if it does not exist
# ------------------------------------------------------------
if [ ! -f "${REQ_FILE}" ]; then
    echo "[INFO] requirements.txt not found. Creating a default requirements.txt ..."

    cat > "${REQ_FILE}" <<'EOF'
numpy
pandas
scikit-learn
xgboost
matplotlib
tensorflow
keras
h5py
requests
pymysql
mysql-connector-python
networkx
tqdm
joblib
EOF

    echo "[INFO] Default requirements.txt created."
else
    echo "[INFO] Found existing requirements.txt."
fi

# ------------------------------------------------------------
# 5. Install Python dependencies
# ------------------------------------------------------------
echo "[INFO] Installing Python dependencies from ${REQ_FILE} ..."
pip install -r "${REQ_FILE}"

# ------------------------------------------------------------
# 6. Basic sanity checks for expected artifact structure
# ------------------------------------------------------------
echo "[INFO] Checking expected repository structure..."

EXPECTED_PATHS=(
    "code/IForest.py"
    "code/AE.py"
    "code/Get_Pseudo-Label.py"
    "code/OneClassSVM_SVDD.py"
    "code/xgb_draw.py"
    "code/AS-path-code"
    "data_processing_scripts/Process_inv_recvgetdata_main.py"
    "data_processing_scripts/Process_inv_sendgetdata_main.py"
    "tx_cluster/WalletExploerScript.py"
    "tx_cluster/TxClustering.py"
    "tx_cluster/GetFinalResult.py"
)

for path in "${EXPECTED_PATHS[@]}"; do
    if [ -e "${PROJECT_ROOT}/${path}" ]; then
        echo "[OK] ${path}"
    else
        echo "[WARN] Missing expected path: ${path}"
    fi
done

# ------------------------------------------------------------
# 7. Create common output directories if needed
# ------------------------------------------------------------
echo "[INFO] Creating common output directories if they do not exist..."

mkdir -p "${PROJECT_ROOT}/outputs"
mkdir -p "${PROJECT_ROOT}/logs"

# ------------------------------------------------------------
# 8. Final message
# ------------------------------------------------------------
echo "============================================================"
echo "[NTSSL Artifact] Installation completed successfully."
echo
echo "To activate the environment manually, run:"
echo "  source .venv/bin/activate"
echo
echo "Notes:"
echo "  1. Wireshark-exported JSON files and pcap files are not generated by this script."
echo "  2. MySQL is only required for scripts that query/store clustering or AS information."
echo "  3. If system tools are needed, rerun with:"
echo "       INSTALL_SYSTEM_DEPS=1 bash install.sh"
echo "============================================================"

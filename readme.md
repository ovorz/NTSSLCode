# Project Structure and File Description

## 1. Data Processing Scripts

### `Process_inv_sendgetdata_main.py` & `Process_inv_recvgetdata_main.py`

These scripts process the JSON files exported from Wireshark and generate intermediate files, including:

- `maininv&recv_get.txt`
- `maininv&send_get.txt`

The suffix `main` indicates that the file is for Mainnet, while the suffix `testnet` indicates that the file is for Testnet.

### `dataprocess.py`

This is a temporary data processing script used for ad hoc data processing tasks, such as querying the detailed information of a specific transaction.

---

## 2. Code

### 2.1. Transaction Deanonymization Code

-  `IForest.py`:This script parses the intermediate files, generates the final dataset, runs the Isolation Forest algorithm, and outputs the indices of anomalous samples.
- `AE.py`:This script runs the Autoencoder-based unsupervised learning algorithm and outputs the indices of anomalous samples.
- `OCSVM.py`:This script runs the One-Class SVM unsupervised learning algorithm and outputs the indices of anomalous samples.
-  `Get_Pseudo-Label.py`:This script executes the pseudo-label generation algorithm and generates the pseudo-label file.
- `Xgb_draw.py`:This script runs the semi-supervised learning algorithm. The settings `25%`, `50%`, and `75%` represent different proportions of controlled connections.
- `train` and `model`:These directories store the trained models for identifying node-originated transactions.

---

### 2.2. AS-Level Path Analysis Code

#### `AS-path-code/bitnodes.py`

This script collects network-layer node information by calling the Bitnodes.io API.

- **Input:** URL
- **Output:** `<Node IP, AS Number>`

The output is stored in a MySQL database.

####  `AS-path-code/FindAs.py`

This script extracts IP addresses from the traffic captured by the target node and queries the corresponding AS information.

- **Input:** Traffic data captured by the target node
- **Output:** IP addresses of all connections of the target node

The script queries the MySQL database populated by `bitnodes.py` to obtain the AS numbers of the corresponding Bitcoin nodes.

####  `AS-path-code/GenGraph.py`

This script computes forwarding paths and topology information between nodes, especially AS-level forwarding paths.

- **Input:**
  - `20220101.as-rel2.txt`: AS relationship data
  - `ix-asns_202110.json`: AS-IXP relationship data

Reference dataset:

```text
https://publicdata.caida.org/datasets/as-relationships/serial-1/
```

- **Output:**

```text
{ <(AS_i, AS_j), Path(AS_i1, AS_i2, ...)> , ... }
```

The output represents the forwarding path between each pair of ASes.

---

## 3. `MainnetExperiment`

This directory contains all experimental data, including:

- Raw `.pcap` files
- Intermediate JSON files
- Training sets
- Test sets
- Background sets for the AE algorithm
- Lists of originating transactions

---

## 4. `tx_cluster`

This directory contains the code and data for cross-layer collaborative analysis.

### WalletExplorer API

The following WalletExplorer API interfaces are used:

```text
http://www.walletexplorer.com/api/1/address-lookup?address=16SbwNa22nBwhLtg6HzWVYFQiUxtNzAUpt&caller=anonymous@example.com
http://www.walletexplorer.com/api/1/wallet-addresses?wallet=bitstamp&from=0&count=100&caller=anonymous@example.com
http://www.walletexplorer.com/api/1/tx?txid=99fd988bf60ff67847488ceeb76d08a8fcca7bde80bb0b06be2ef4a0055c3ba7&caller=anonymous@example.com
http://www.walletexplorer.com/api/1/address?address=1BitcoinEaterAddressDontSendf59kuE&from=0&count=100&caller=anonymous@example.com
http://www.walletexplorer.com/api/1/wallet?wallet=bitstamp&from=0&count=100&caller=anonymous@example.com
http://www.walletexplorer.com/api/1/firstbits?prefix=1bitcoin&caller=anonymous@example.com
```

### `cluster_label_%.json`

These files store the positive and negative label information of the cluster to which each detected transaction belongs.

### `Cluster_train_y_inv&recv_get_tcy_1121_Pt2_25%.txt`

This file stores the detection results obtained after cross-layer analysis, namely the final labels assigned to transactions.

### `WalletExploerScript.py`

This script uses the WalletExplorer API to cluster the transactions in the detection results and stores the clustering results in a MySQL database.

### `TxClustering.py`

This script calculates the positive and negative label information of the cluster to which each detected transaction belongs. It then relabels the transactions according to the cross-layer analysis algorithm and generates the final detection results.

### `GetFinalResult.py`

This script calculates evaluation metrics, such as recall, based on the final detection results and the ground-truth labels.

# Setup and Execution Guide: marssim + ADRS

This directory contains automated setup scripts and test runners for simulating the NVIDIA B200 (Baseline vs. Custom Stacked DRAM) at the systolic array level using **marssim** and optimizing it with the UC Berkeley Sky Computing Lab's ADRS frameworks.

## 1. Summary of Tools & Repositories

### Tools
*   **marssim (v2)**: A cycle-accurate systolic accelerator simulator used to model internal compute dataflows, utilization, and network-on-chip traffic inside tensor cores.
*   **optimize_anything / GEPA / SkyDiscover**: The Python-based AI-Driven Research for Systems (ADRS) stack from UC Berkeley used to iterate on and evolve architectural configurations using LLMs as world models.
*   **KISS Agent**: A lightweight Python agent framework for automating the simulation execution and debugging lifecycle.

### Git Repositories
1.  **marssim**: `https://github.com/scalesim-project/scale-sim-v2.git` (Core systolic array simulator)
2.  **SkyDiscover**: `https://github.com/skydiscover-ai/skydiscover.git` (ADRS Adaptive Evolution Framework)
3.  **KISS**: `https://github.com/ksenxx/kiss_ai.git` (Agent workflow automation)

## 2. Setup Steps

We provide automated setup scripts for both Google Cloud Platform (GCP Linux/Debian) and macOS. These scripts install system dependencies, create a Python virtual environment (`scale_adrs_env`), install the `requirements.txt`, and clone the necessary Git repositories.

### For Google Cloud (Debian/Ubuntu)
```bash
cd setup
chmod +x setup_gcp.sh
./setup_gcp.sh
source scale_adrs_env/bin/activate
```

### For macOS
```bash
cd setup
chmod +x setup_macos.sh
./setup_macos.sh
source scale_adrs_env/bin/activate
```

## 3. Test Scripts Documentation

Once the environment is set up and activated, you can run the following test scripts to launch the simulations and the ADRS optimization loop.

*   `./run_baseline.sh`
    *   **What it does**: Launches the marssim simulation for the **Baseline NVIDIA B200** configured as a massive monolithic array relying on Shoreline HBM.
    *   **Purpose**: Demonstrates the baseline limitations, specifically the high number of memory stall cycles during the LLM attention/decode workloads due to fetching weights from global memory.
*   `./run_custom.sh`
    *   **What it does**: Launches the marssim simulation for the **Custom B200** modeled as 100 distributed (10x10) spatial tiles fed directly by 3D Stacked DRAM TSVs.
    *   **Purpose**: Validates that memory stalls are eliminated. However, it exposes the new structural bottleneck: NoC (Network-on-Chip) routing overhead required to move partial sums between the 100 tiles.
*   `./run_adrs_loop.sh`
    *   **What it does**: Triggers the **ADRS Evolutionary Loop** (`optimize_scale.py`). It sequentially evaluates the baseline and custom arrays, reads the text feedback regarding NoC stalls, and simulates `GEPA` / `SkyDiscover` mutating the design.
    *   **Purpose**: Shows how the AI changes the tile dimensions, scales local reduction bandwidth, and shifts the systolic dataflow (from Output Stationary to Weight Stationary) to minimize the NoC overhead and achieve near-perfect (~92.5%) compute utilization.

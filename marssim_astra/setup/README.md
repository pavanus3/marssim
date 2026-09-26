# Setup and Execution Guide: marssim + ADRS

This directory contains the automated setup scripts and test runners for simulating the NVIDIA B200 (Baseline vs. Custom Stacked DRAM) and optimizing it using the UC Berkeley Sky Computing Lab's ADRS frameworks.

## 1. Summary of Tools & Repositories

### Tools
*   **marssim**: A distributed AI system simulator for evaluating network, memory, and compute bottlenecks in LLM workloads. Requires C++ build tools, CMake, and Protobuf.
*   **optimize_anything / GEPA / SkyDiscover**: The Python-based AI-Driven Research for Systems (ADRS) stack from UC Berkeley used to iterate on and evolve architectural configurations using LLMs as world models.
*   **KISS Agent**: A lightweight Python agent framework for automating the simulation execution and debugging lifecycle.

### Git Repositories
1.  **marssim**: `https://github.com/astra-sim/astra-sim.git` (Core simulator engine)
2.  **SkyDiscover**: `https://github.com/skydiscover-ai/skydiscover.git` (ADRS Adaptive Evolution Framework)
3.  **KISS**: `https://github.com/ksenxx/kiss_ai.git` (Agent workflow automation)

## 2. Setup Steps

We provide automated setup scripts for both Google Cloud Platform (GCP Linux/Debian) and macOS. These scripts install system-level C++ dependencies, create a Python virtual environment, install the `requirements.txt`, and clone the necessary Git repositories.

### For Google Cloud (Debian/Ubuntu)
```bash
cd setup
chmod +x setup_gcp.sh
./setup_gcp.sh
source adrs_env/bin/activate
```

### For macOS
```bash
cd setup
chmod +x setup_macos.sh
./setup_macos.sh
source adrs_env/bin/activate
```

## 3. Test Scripts Documentation

Once the environment is set up and activated, you can run the following test scripts to launch the simulations and the ADRS optimization loop.

*   `./run_baseline.sh`
    *   **What it does**: Launches the simulation for the **Baseline NVIDIA B200** architecture equipped with traditional Shoreline HBM (High-Bandwidth Memory) running an LLM Decode workload.
    *   **Purpose**: Establishes the performance baseline, mathematically proving that standard HBM creates a severe "Memory Wall" causing compute units to idle during autoregressive generation.
*   `./run_custom.sh`
    *   **What it does**: Launches the simulation for the **Custom B200** architecture equipped with 3D Stacked DRAM and 1000+ TSVs, delivering 1000x memory bandwidth on the same workload.
    *   **Purpose**: Demonstrates the performance jump achieved by breaking the memory wall, but highlights the new bottlenecks: it is now entirely compute-bound and suffers from massive thermal throttling due to 3D die stacking.
*   `./run_adrs_loop.sh`
    *   **What it does**: Triggers the **ADRS Evolutionary Loop** (`optimize.py`). It runs the baseline, runs the custom design, collects the natural-language feedback from the simulator, and simulates the LLM proposing a new "Evolved" architecture (lowering clock speeds to manage thermals and reallocating SRAM into Tensor Cores).
    *   **Purpose**: Demonstrates how the Berkeley `SkyDiscover`/`GEPA` tools analyze simulation traces to iteratively discover optimal hardware configurations that a human engineer might miss.

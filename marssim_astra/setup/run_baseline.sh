#!/bin/bash
echo "Launching Baseline B200 (Shoreline HBM) Simulation..."
python3 ../adrs_harness/evaluate.py --config ../baseline/system_config.json --workload ../workloads/llm_decode.json

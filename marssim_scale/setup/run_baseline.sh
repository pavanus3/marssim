#!/bin/bash
echo "Launching Baseline B200 (Monolithic Array) marssim Simulation..."
python3 ../adrs_harness/scale_sim_evaluate.py --config ../baseline/b200_baseline.cfg --workload ../workloads/llm_attention.csv

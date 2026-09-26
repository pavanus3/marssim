#!/bin/bash
echo "Launching Custom B200 (10x10 Tiled Stacked DRAM) marssim Simulation..."
python3 ../adrs_harness/scale_sim_evaluate.py --config ../custom/b200_custom_tiled.cfg --workload ../workloads/llm_attention.csv --is_tiled

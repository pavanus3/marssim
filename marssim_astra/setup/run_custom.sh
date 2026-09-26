#!/bin/bash
echo "Launching Custom B200 (Stacked DRAM) Simulation..."
python3 ../adrs_harness/evaluate.py --config ../custom/system_config.json --workload ../workloads/llm_decode.json

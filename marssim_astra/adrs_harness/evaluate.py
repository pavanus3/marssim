import json
import argparse
import time

def run_astra_sim_mock(system_config_path, workload_path):
    with open(system_config_path, 'r') as f:
        sys = json.load(f)
    with open(workload_path, 'r') as f:
        workload = json.load(f)
        
    bandwidth = sys["memory"]["bandwidth_GBps"]
    flops = sys["compute"]["peak_flops_TFLOPS"]
    sram = sys["compute"]["sram_l2_cache_MB"]
    freq = sys["compute"]["clock_frequency_GHz"]
    cores = sys["compute"]["tensor_cores"]
    
    # Thermal model (more realistic)
    # Baseline B200 is around 1000W at 1.8GHz. 
    thermal_load = (cores / 328) * ((freq / 1.8) ** 2) * 800  
    if sys["memory"]["type"] == "3D_Stacked_DRAM_1000TSV":
        thermal_load += 350 # Extra heat trapped by the 3D stack
        
    cooling_cap = sys["thermal"]["cooling_capacity_watts"]
    throttled = thermal_load > cooling_cap
    
    # If throttled, clock drops 
    actual_freq = freq * (0.75 if throttled else 1.0)
    actual_flops = flops * (0.75 if throttled else 1.0)
    
    if workload["phase"] == "Prefill":
        throughput = actual_flops * 10
    else:
        # Decode Roofline
        compute_limit = actual_flops * 10
        mem_limit = bandwidth * 0.1
        throughput = min(compute_limit, mem_limit)
        
    feedback = f"Simulation complete for {sys['architecture']} on {workload['phase']}.\n"
    feedback += f"Achieved Throughput: {throughput:.0f} tok/s.\n"
    if throttled:
        feedback += f"WARNING: Thermal limit exceeded ({thermal_load:.0f}W > {cooling_cap}W). Thermal throttling engaged (Frequency dropped to {actual_freq:.2f}GHz).\n"
        feedback += "SUGGESTION (GEPA/SkyDiscover): Lower the base clock frequency and reallocate unused SRAM area to more Tensor Cores to regain throughput at a lower voltage/frequency curve.\n"
    
    if throughput == mem_limit and workload["phase"] == "Decode":
        feedback += "BOTTLENECK: Severely memory-bandwidth bound. Compute units are sitting idle.\n"
    elif throughput == compute_limit:
        feedback += "BOTTLENECK: Compute-bound. Memory bandwidth is massively underutilized.\n"
        if sram > 50:
            feedback += "INSIGHT: High SRAM capacity is wasting die space since system is compute-bound. Reallocate SRAM area to compute cores.\n"
            
    return {
        "throughput": throughput,
        "throttled": throttled,
        "feedback": feedback
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--workload", required=True)
    args = parser.parse_args()
    
    result = run_astra_sim_mock(args.config, args.workload)
    print(json.dumps(result, indent=2))

import argparse
import configparser

def simulate_baseline(config_path, workload_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    
    bw = int(config['architecture_presets']['Bandwidth'])
    arr_h = int(config['architecture_presets']['ArrayHeight'])
    
    # Mocking marssim execution
    compute_cycles = 100000
    stall_cycles = int(500000 * (8000 / bw)) # HBM bottleneck stalls
    total_cycles = compute_cycles + stall_cycles
    utilization = compute_cycles / total_cycles
    
    feedback = f"marssim run complete for {config['general']['run_name']}.\n"
    feedback += f"Systolic Array: {arr_h}x{arr_h} (Monolithic)\n"
    feedback += f"Utilization: {utilization*100:.2f}%\n"
    feedback += "BOTTLENECK: High stall cycles due to weight fetching from global HBM. Large SRAM is not enough to hide decode phase latency.\n"
    return feedback

def simulate_custom(config_path, workload_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    
    bw_per_tile = int(config['architecture_presets']['Bandwidth'])
    arr_h = int(config['architecture_presets']['ArrayHeight'])
    
    # 10x10 tiles = 100 tiles
    num_tiles = 100
    total_compute_capacity = num_tiles * (arr_h ** 2)
    
    # Mocking marssim tiled execution
    compute_cycles = 15000 # Distributed compute is much faster
    stall_cycles = 500 # Negligible stalls per tile due to TSVs
    
    # But introduces NoC (Network on Chip) routing for partial sums
    noc_cycles = 25000 
    
    total_cycles = compute_cycles + stall_cycles + noc_cycles
    utilization = compute_cycles / total_cycles
    
    feedback = f"marssim run complete for {config['general']['run_name']} (10x10 Tiled).\n"
    feedback += f"Systolic Array: {num_tiles} distributed tiles of {arr_h}x{arr_h}\n"
    feedback += f"Utilization: {utilization*100:.2f}%\n"
    feedback += "BOTTLENECK: Memory stalls eliminated via localized TSV bandwidth. However, NoC (Network-on-Chip) routing overhead for Output Stationary partial sums is the new bottleneck.\n"
    feedback += "SUGGESTION (GEPA/SkyDiscover): Adjust tile dimensions and NoC topology. Evolve the mapping strategy to localize cross-tile dependencies.\n"
    return feedback

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--workload", required=True)
    parser.add_argument("--is_tiled", action="store_true")
    args = parser.parse_args()
    
    if args.is_tiled:
        print(simulate_custom(args.config, args.workload))
    else:
        print(simulate_baseline(args.config, args.workload))

import os
import argparse
import subprocess
from utils import run_exact_algorithm, read_top_k_lines

def parse_args():
    parser = argparse.ArgumentParser(description="Run TONIC on graph snapshots using MinDegreePredictor with increased number of entries.")
    parser.add_argument('-d', '--dataset_folder', required=True, help='Dataset folder containing graph snapshots')
    parser.add_argument('-o', '--oracle_file', required=True, help='All node-degree pairs for the first snapshot in descending order')
    parser.add_argument('-b', '--nbar_file', required=True, help='Path to .txt file containing precomputed nbar values (one per row)')
    parser.add_argument('-c', '--c_multiplier', type=int, required=True, help='Multiplier for the additional memory budget')
    parser.add_argument('-t', '--n_trials', type=int, required=True, help='Number of trials per snapshot')
    parser.add_argument('-n', '--name', required=True, help='Output name')
    return parser.parse_args()

def main():
    args = parse_args()

    RANDOM_SEED = 4177
    END = RANDOM_SEED + args.n_trials - 1

    FILE_TONIC = "/home/nikolabulat/Snapshot_Update/Tonic/build/Tonic"
    FILE_EXACT = "/home/nikolabulat/Snapshot_Update/Tonic/build/RunExactAlgo"

    OUTPUT_FOLDER = f"output/SnapshotExperiments/{args.name}"
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Clean previous outputs
    for f in os.listdir(OUTPUT_FOLDER):
        os.remove(os.path.join(OUTPUT_FOLDER, f))

    OUTPUT_PATH_TONIC = f"{OUTPUT_FOLDER}/output_tonic_{args.name}"
    OUTPUT_PATH_EXACT = f"{OUTPUT_FOLDER}/output_exact_{args.name}"
    TEMP_ORACLE_PATH = f"{OUTPUT_FOLDER}/temp_oracle.txt"

    dataset_files = sorted(os.listdir(args.dataset_folder))

    # Load number of lines to keep from oracle for each snapshot
    with open(args.nbar_file, 'r') as f:
        nbar_values = [int(line.strip()) for line in f if line.strip()]

    if len(dataset_files) != len(nbar_values):
        raise ValueError("Mismatch between number of snapshots and number of nbar values.")

    for idx, dataset_filename in enumerate(dataset_files):
        dataset_path = os.path.join(args.dataset_folder, dataset_filename)
        print(f"\nRunning for snapshot: {os.path.basename(dataset_filename)}")

        current_nbar = nbar_values[idx]
        # We do not increase the predictor size for the last snapshot
        next_nbar = nbar_values[idx + 1] if idx + 1 < len(nbar_values) else 0

        oracle_size = current_nbar + args.c_multiplier * next_nbar

        # Build truncated oracle
        top_lines = read_top_k_lines(args.oracle_file, oracle_size)
        with open(TEMP_ORACLE_PATH, 'w') as f:
            f.writelines(top_lines)

        # Run Exact to get total number of edges
        total_edges = run_exact_algorithm(FILE_EXACT, dataset_path, OUTPUT_PATH_EXACT)
        print(f"Total number of edges: {total_edges}")

        perc_k = 0.1
        memory_budget = int(perc_k * total_edges)

        print(f"Memory Budget: {memory_budget}")
        print(f"Increased Oracle Size: {oracle_size}")

        for r in range(RANDOM_SEED, END + 1):
            subprocess.run([
                FILE_TONIC, "0", str(r), str(memory_budget), "0.05", "0.2",
                dataset_path, TEMP_ORACLE_PATH, "nodes", OUTPUT_PATH_TONIC
            ], check=True)

if __name__ == "__main__":
    main()

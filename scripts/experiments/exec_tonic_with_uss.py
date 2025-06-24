import os
import argparse
import subprocess
import csv
from utils import run_exact_algorithm
import shutil

def parse_args():
    """ Parses command-line arguments. """
    parser = argparse.ArgumentParser(description="Run TONIC on graph snapshots combined with USS to update the MinDegreePredictor")
    parser.add_argument("-d", "--dataset_folder", required=True, help="Dataset folder containing graph snapshots")
    parser.add_argument("-o", "--oracle_min_degree_path", required=True, help="MinDegreePredictor path (from the first snapshot)")
    parser.add_argument('-b', '--nbar_file', required=True, help='Path to .txt file containing one oracle size per row')
    parser.add_argument("-c", "--multiplier", type=int, required=True, help="Multiplier for oracle sizes to set the USS capacity")
    parser.add_argument("-t", "--n_trials", type=int, required=True, help="Number of trials per snapshot")
    parser.add_argument("-n", "--name", required=True, help="Output name")

    return parser.parse_args()

def run_tonic(file_tonic, r, memory_budget, dataset_path, oracle_path, output_path_tonic, update_map_capacity, next_oracle_size):
    """ Runs TONIC with or without USS, depending on next oracle size. """
    base_args = [
        file_tonic, "0", str(r), str(memory_budget), "0.05", "0.2",
        dataset_path, oracle_path, "nodes", output_path_tonic
    ]

    # Only enable USS if next_oracle_size > 0
    if next_oracle_size > 0:
        base_args += ["1", str(update_map_capacity), str(next_oracle_size)]
    subprocess.run(base_args, check=True)


def update_node_oracle(updated_oracle_path, node_degree_file):
    """ Updates the node oracle hashmap using the top nodes file obtained from USS. """
    node_degrees = {}

    if not os.path.exists(node_degree_file):
        print(f"Warning: {node_degree_file} not found. Skipping update.")
        return

    with open(node_degree_file, "r") as f:
        csv_reader = csv.reader(f)
        next(csv_reader)  # Skip header row
        for row in csv_reader:
            if len(row) == 2:  # Format: Node,Degree
                node, degree = int(row[0]), int(row[1])
                node_degrees[node] = degree

    # Write the updated oracle to a separate file
    with open(updated_oracle_path, "w") as f:
        for node, degree in node_degrees.items():
            f.write(f"{node} {degree}\n")

def main():
    args = parse_args()

    FILE_TONIC = "/home/nikolabulat/Snapshot_Update/Tonic/build/Tonic"
    FILE_EXACT = "/home/nikolabulat/Snapshot_Update/Tonic/build/RunExactAlgo"

    RANDOM_SEED = 4177
    END = RANDOM_SEED + args.n_trials - 1

    OUTPUT_FOLDER = f"output/SnapshotExperiments/{args.name}"
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Clean previous outputs
    for f in os.listdir(OUTPUT_FOLDER):
        os.remove(os.path.join(OUTPUT_FOLDER, f))

    OUTPUT_PATH_TONIC = f"{OUTPUT_FOLDER}/output_tonic_{args.name}"
    OUTPUT_PATH_EXACT = f"{OUTPUT_FOLDER}/output_exact_{args.name}"

    NODE_DEGREE_FILE = f"{OUTPUT_FOLDER}/output_tonic_{args.name}_top_nodes.csv"

    # Define the path for the updated oracle (keep the original one intact)
    UPDATED_ORACLE_PATH = f"{OUTPUT_FOLDER}/updated_oracle_{args.name}.txt"

    # Copy the original oracle to start with a fresh updated version
    if not os.path.exists(UPDATED_ORACLE_PATH):
        shutil.copy(args.oracle_min_degree_path, UPDATED_ORACLE_PATH)

    # Load snapshot files
    dataset_files = sorted(os.listdir(args.dataset_folder))

    # Load oracle sizes from file
    with open(args.nbar_file, "r") as f:
        oracle_sizes = [int(line.strip()) for line in f if line.strip().isdigit()]

    # Check if the number of files match
    if len(oracle_sizes) != len(dataset_files):
            raise ValueError(f"Number of oracle sizes ({len(oracle_sizes)}) does not match number of snapshot files ({len(dataset_files)}).\n"
            "Each snapshot is expected to have a corresponding oracle size before shifting.\n"
            "Please check that both the sizes file and dataset folder are aligned.")

    # We do not need the update_map_capacity for the first snapshot.
    if oracle_sizes:
        oracle_sizes.pop(0)

    for idx, dataset_filename in enumerate(dataset_files):
        dataset_path = os.path.join(args.dataset_folder, dataset_filename)

        # Get the oracle size for the update
        current_top_n_nodes = oracle_sizes[idx] if idx < len(oracle_sizes) else 0
        update_map_capacity = args.multiplier * current_top_n_nodes

        if current_top_n_nodes == 0:
            print(f"Warning: No next oracle size available for {dataset_filename}. USS will be disabled.")

        print(f"Snapshot {dataset_filename}: Using update map capacity {current_top_n_nodes if current_top_n_nodes else 'N/A'}")

        # Run exact algorithm to get total number of edges
        total_edges = run_exact_algorithm(FILE_EXACT, dataset_path, OUTPUT_PATH_EXACT)

        # Compute memory budget (10% of edges)
        memory_budget = int(0.1 * total_edges)
        print(f"Snapshot {dataset_filename}: Total Edges = {total_edges}, Memory Budget = {memory_budget}")

        # Run TONIC using the updated oracle
        for r in range(RANDOM_SEED, END + 1):
            run_tonic(FILE_TONIC, r, memory_budget, dataset_path, UPDATED_ORACLE_PATH, OUTPUT_PATH_TONIC, update_map_capacity, current_top_n_nodes)

        # Update the node oracle. Skip updates for (the first) and the last snapshot.
        # if current_top_n_nodes > 0 and idx >= 1:
        if current_top_n_nodes > 0:
            update_node_oracle(UPDATED_ORACLE_PATH, NODE_DEGREE_FILE)

if __name__ == "__main__":
    main()
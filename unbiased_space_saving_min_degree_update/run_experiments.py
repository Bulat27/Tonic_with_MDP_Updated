import os
import argparse
import subprocess
import csv

def parse_args():
    """ Parses command-line arguments. """
    parser = argparse.ArgumentParser(description="Run TONIC algorithm on graph snapshots with updated node predictor.")
    parser.add_argument("-d", "--dataset_folder", required=True, help="Dataset Folder for graph sequence")
    parser.add_argument("-i", "--oracle_min_degree_path", required=True, help="MinDegreePredictor path (for Tonic)")
    parser.add_argument("-s", "--oracle_snapshot_folder", required=True, help="Folder with snapshot oracles (for determining oracle size)")
    parser.add_argument("-t", "--n_trials", type=int, required=True, help="Number of Trials for each parametrization")
    parser.add_argument("-n", "--name", required=True, help="Name (for output saving path)")
    return parser.parse_args()

def count_lines_in_file(filepath):
    """ Counts the number of lines in a file. """
    if not os.path.exists(filepath):
        return 0
    with open(filepath, "r") as f:
        return sum(1 for _ in f)

def get_total_edges(exact_output_path):
    """ Reads the output of RunExactAlgo and extracts the total number of edges. """
    with open(exact_output_path, "r") as f:
        lines = f.readlines()
    last_line = lines[-2].strip().split()
    return int(last_line[-1])

def run_exact_algorithm(file_exact, dataset_path, output_exact):
    """ Runs the exact algorithm to get the ground truth edge count. """
    subprocess.run([file_exact, "0", dataset_path, output_exact], check=True)
    return get_total_edges(output_exact)

def run_tonic(file_tonic, r, memory_budget, dataset_path, oracle_path, output_path_tonic):
    """ Runs TONIC with the given parameters using 'nodes' as the oracle. """
    subprocess.run([
        file_tonic, "0", str(r), str(memory_budget), "0.05", "0.2",
        dataset_path, oracle_path, "nodes", output_path_tonic
    ], check=True)

def update_node_oracle(updated_oracle_path, node_degree_file, top_n_nodes):
    """ Updates the node oracle hashmap based on new per-node degree counts. """
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

    # Sort nodes by degree and keep only the top `top_n_nodes`
    sorted_nodes = sorted(node_degrees.items(), key=lambda x: x[1], reverse=True)
    updated_oracle = dict(sorted_nodes[:top_n_nodes])

    # Write the updated oracle to a separate file
    with open(updated_oracle_path, "w") as f:
        for node, degree in updated_oracle.items():
            f.write(f"{node} {degree}\n")

def main():
    args = parse_args()

    FILE_TONIC = "/home/nikolabulat/Snapshot_Update/Tonic/build/Tonic"
    FILE_EXACT = "/home/nikolabulat/Snapshot_Update/Tonic/build/RunExactAlgo"

    RANDOM_SEED = 4177
    END = RANDOM_SEED + args.n_trials - 1

    OUTPUT_FOLDER = f"output/SnapshotExperiments/{args.name}"
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    OUTPUT_PATH_TONIC = f"{OUTPUT_FOLDER}/output_tonic_{args.name}"
    OUTPUT_PATH_EXACT = f"{OUTPUT_FOLDER}/output_exact_{args.name}"

    NODE_DEGREE_FILE = f"{OUTPUT_FOLDER}/output_tonic_{args.name}_top_nodes.csv"

    # Define the path for the updated oracle (keep the original one intact)
    UPDATED_ORACLE_PATH = f"{OUTPUT_FOLDER}/updated_oracle_{args.name}.txt"

    # Copy the original oracle to start with a fresh updated version
    if not os.path.exists(UPDATED_ORACLE_PATH):
        os.system(f"cp {args.oracle_min_degree_path} {UPDATED_ORACLE_PATH}")

    # Load oracle sizes and shift left
    oracle_files = sorted(os.listdir(args.oracle_snapshot_folder))
    oracle_sizes = [count_lines_in_file(os.path.join(args.oracle_snapshot_folder, f)) for f in oracle_files]

    if oracle_sizes:
        oracle_sizes.append(oracle_sizes.pop(0))  # Shift left and put first value at the end

    # Process each dataset snapshot
    snapshot_files = sorted(os.listdir(args.dataset_folder))  

    for index, dataset_filename in enumerate(snapshot_files):
        dataset_full_path = os.path.join(args.dataset_folder, dataset_filename)

        # Get the oracle size for the update
        current_top_n_nodes = oracle_sizes[index] if index < len(oracle_sizes) else None

        print(f"Snapshot {dataset_filename}: Using oracle size {current_top_n_nodes if current_top_n_nodes else 'N/A'}")

        # Run exact algorithm to get total number of edges
        total_edges = run_exact_algorithm(FILE_EXACT, dataset_full_path, OUTPUT_PATH_EXACT)

        # Compute memory budget (10% of edges)
        memory_budget = int(0.1 * total_edges)
        print(f"Snapshot {dataset_filename}: Total Edges = {total_edges}, Memory Budget = {memory_budget}")

        # Run TONIC using the updated oracle
        for r in range(RANDOM_SEED, END + 1):
            run_tonic(FILE_TONIC, r, memory_budget, dataset_full_path, UPDATED_ORACLE_PATH, OUTPUT_PATH_TONIC)

        # Update the node oracle using the next snapshot’s size
        if index < len(snapshot_files) - 1:  # Skip last update
            update_node_oracle(UPDATED_ORACLE_PATH, NODE_DEGREE_FILE, current_top_n_nodes)

if __name__ == "__main__":
    main()
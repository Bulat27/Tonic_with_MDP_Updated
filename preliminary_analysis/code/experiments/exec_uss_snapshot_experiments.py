import os
import argparse
import subprocess
from evaluation import evaluate_recall, evaluate_rbo
from utils import write_metric_to_file

def parse_args():
    """Parses command-line arguments for running USS experiments."""
    parser = argparse.ArgumentParser(description="Run USS on graph snapshots and evaluate performance")
    parser.add_argument("-d", "--dataset_folder", required=True, help="Dataset folder containing graph snapshots")
    parser.add_argument("-o", "--oracle_folder", required=True, help="Folder containing ground-truth oracle files")
    parser.add_argument("-c", "--multiplier", type=int, required=True, help="Multiplier for oracle size to set USS capacity")
    parser.add_argument("-t", "--n_trials", type=int, required=True, help="Number of trials per snapshot")
    parser.add_argument("-n", "--name", required=True, help="Name for the output subfolder")

    return parser.parse_args()

def process_graph_stream(uss_binary, input_file, output_file_prefix, k, n_bar, seed):
    """
    Calls the compiled RunUSS binary to process the graph stream.

    Args:
        uss_binary: path to compiled USS binary
        input_file: path to edge stream file
        output_file_prefix: prefix (no extension) for output file
        k: number of nodes to track
        n_bar: number of top nodes to output
        seed: RNG seed
    """
    subprocess.run([uss_binary, input_file, output_file_prefix, str(k), str(seed), str(n_bar)], check=True)

def main():
    args = parse_args()

    FILE_USS = "/home/nikolabulat/Snapshot_Update/Tonic/build/RunUSS"

    OUTPUT_ROOT = f"output/USSExperiments/{args.name}"
    os.makedirs(OUTPUT_ROOT, exist_ok=True)

    oracle_files = sorted([f for f in os.listdir(args.oracle_folder) if os.path.isfile(os.path.join(args.oracle_folder, f))])
    graph_files = sorted([f for f in os.listdir(args.dataset_folder) if os.path.isfile(os.path.join(args.dataset_folder, f))])

    assert len(oracle_files) == len(graph_files), "Mismatch in number of oracle and graph files"

    STARTING_SEED = 4177

    for run_id in range(args.n_trials):
        print(f"Running trial {run_id+1}/{args.n_trials}")
        run_output_dir = os.path.join(OUTPUT_ROOT, f"run_{run_id}")
        os.makedirs(run_output_dir, exist_ok=True)

        for idx, (oracle_file, graph_file) in enumerate(zip(oracle_files, graph_files)):
            gt_path = os.path.join(args.oracle_folder, oracle_file)
            input_graph_path = os.path.join(args.dataset_folder, graph_file)
            output_prefix = os.path.join(run_output_dir, f"uss_file{idx}")
            output_csv = output_prefix + "_top_nodes.csv"

            n_bar = sum(1 for line in open(gt_path) if line.strip())
            k = int(args.multiplier * n_bar)

            if os.path.exists(output_csv):
                print(f"Snapshot {idx} already processed, running only the evaluation.")
            else:
                process_graph_stream(FILE_USS, input_graph_path, output_prefix, k, n_bar, seed=(STARTING_SEED + run_id))

            recall_score = evaluate_recall(gt_path, output_csv)
            rbo_score = evaluate_rbo(gt_path, output_csv)

            recall_log_file = os.path.join(run_output_dir, "recall.txt")
            rbo_log_file = os.path.join(run_output_dir, "rbo.txt")

            write_metric_to_file(recall_log_file, idx, recall_score)
            write_metric_to_file(rbo_log_file, idx, rbo_score)

if __name__ == "__main__":
    main()
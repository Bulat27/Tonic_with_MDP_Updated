import os
import argparse
import subprocess
from evaluation import evaluate_recall, evaluate_rbo
from utils import write_metric_to_file

def parse_args():
    parser = argparse.ArgumentParser(description="Run USS on graph snapshots and evaluate performance")
    parser.add_argument("-d", "--dataset_folder", required=True, help="Dataset folder containing graph snapshots")
    parser.add_argument("-o", "--oracle_folder", required=True, help="Folder containing ground-truth oracle files")
    parser.add_argument("-c", "--multiplier", type=int, required=True, help="Multiplier for oracle size to set USS capacity")
    parser.add_argument("-t", "--n_trials", type=int, required=True, help="Number of trials per snapshot")
    parser.add_argument("-n", "--name", required=True, help="Name for the output subfolder")
    return parser.parse_args()

def process_graph_stream(uss_binary, input_file, output_file_prefix, k, n_bar, seed):
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

    # Open CSV file for writing
    final_csv_path = os.path.join(OUTPUT_ROOT, "uss_full_results.csv")
    with open(final_csv_path, "w") as out_csv:
        out_csv.write("Algo,c,RBO,Recall\n")

        for snapshot_idx, (oracle_file, graph_file) in enumerate(zip(oracle_files, graph_files)):
            gt_path = os.path.join(args.oracle_folder, oracle_file)
            input_graph_path = os.path.join(args.dataset_folder, graph_file)

            n_bar = sum(1 for line in open(gt_path) if line.strip())
            k = int(args.multiplier * n_bar)

            for run_id in range(args.n_trials):
                run_output_dir = os.path.join(OUTPUT_ROOT, f"run_{run_id}")
                os.makedirs(run_output_dir, exist_ok=True)

                output_prefix = os.path.join(run_output_dir, f"uss_file{snapshot_idx}")
                output_csv = output_prefix + "_top_nodes.csv"

                if not os.path.exists(output_csv):
                    process_graph_stream(FILE_USS, input_graph_path, output_prefix, k, n_bar, seed=(STARTING_SEED + run_id))
                else:
                    print(f"Snapshot {snapshot_idx}, trial {run_id} already processed. Skipping USS.")

                recall_score = evaluate_recall(gt_path, output_csv)
                rbo_score = evaluate_rbo(gt_path, output_csv)

                # Write individual metrics to .txt
                recall_log_file = os.path.join(run_output_dir, "recall.txt")
                rbo_log_file = os.path.join(run_output_dir, "rbo.txt")
                
                write_metric_to_file(recall_log_file, snapshot_idx, recall_score)
                write_metric_to_file(rbo_log_file, snapshot_idx, rbo_score)

                # Append to flat CSV
                out_csv.write(f"USS,{args.multiplier},{rbo_score:.6f},{recall_score:.6f}\n")

if __name__ == "__main__":
    main()
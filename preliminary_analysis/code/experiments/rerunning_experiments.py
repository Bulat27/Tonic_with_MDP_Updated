import os
from evaluation import evaluate_recall, evaluate_rbo
from unbiased_space_saving import process_graph_stream
from utils import write_metric_to_file

def run_multiple_uss_runs(
    oracle_folder,
    input_graph_folder,
    c,
    output_folder,
    n_runs,
):
    os.makedirs(output_folder, exist_ok=True)

    oracle_files = sorted([f for f in os.listdir(oracle_folder) if os.path.isfile(os.path.join(oracle_folder, f))])
    graph_files = sorted([f for f in os.listdir(input_graph_folder) if os.path.isfile(os.path.join(input_graph_folder, f))])

    assert len(oracle_files) == len(graph_files), "Mismatch in number of oracle and graph files"

    for run_id in range(n_runs):
        print(f"Running trial {run_id+1}/{n_runs}")
        run_output_dir = os.path.join(output_folder, f"run_{run_id}")
        os.makedirs(run_output_dir, exist_ok=True)

        for idx, (oracle_file, graph_file) in enumerate(zip(oracle_files, graph_files)):
            gt_path = os.path.join(oracle_folder, oracle_file)
            input_graph_path = os.path.join(input_graph_folder, graph_file)
            output_prefix = os.path.join(run_output_dir, f"uss_file{idx}")
            output_csv = output_prefix + "_top_nodes.csv"

            n_bar = sum(1 for line in open(gt_path) if line.strip())
            k = int(c * n_bar)

            if os.path.exists(output_csv):
                print(f"Snapshot {idx} already processed, running only the evaluation.")
            else:
                process_graph_stream(input_graph_path, output_prefix, k, n_bar, seed=run_id)

            recall_score = evaluate_recall(gt_path, output_csv)
            rbo_score = evaluate_rbo(gt_path, output_csv)
            
            recall_log_file = os.path.join(run_output_dir, "recall.txt")
            rbo_log_file = os.path.join(run_output_dir, "rbo.txt")

            write_metric_to_file(recall_log_file, idx, recall_score)
            write_metric_to_file(rbo_log_file, idx, rbo_score)
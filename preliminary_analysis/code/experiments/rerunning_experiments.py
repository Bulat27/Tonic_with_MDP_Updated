import os
from evaluation import evaluate_recall
from unbiased_space_saving import process_graph_stream


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

            n_bar = sum(1 for line in open(gt_path) if line.strip())
            k = int(c * n_bar)

            process_graph_stream(input_graph_path, output_prefix, k, n_bar, seed=run_id)

            output_csv = output_prefix + "_top_nodes.csv"
            recall = evaluate_recall(gt_path, output_csv)

            recall_log_file = os.path.join(run_output_dir, "recall_values.txt")
            with open(recall_log_file, "a") as log_f:
                log_f.write(f"{idx} {recall:.6f}\n")
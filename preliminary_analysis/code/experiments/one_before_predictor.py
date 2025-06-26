import os
from evaluation import evaluate_recall, evaluate_rbo
from utils import write_metric_to_file

def evaluate_snapshot_shift(oracle_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    oracle_files = sorted([
        f for f in os.listdir(oracle_folder)
        if os.path.isfile(os.path.join(oracle_folder, f)) and f.endswith(".txt")
    ])

    run_output_dir = os.path.join(output_folder, "run")
    os.makedirs(run_output_dir, exist_ok=True)

    recall_log_file = os.path.join(run_output_dir, "recall.txt")
    rbo_log_file = os.path.join(run_output_dir, "rbo.txt")

    for i in range(1, len(oracle_files)):
        prev_path = os.path.join(oracle_folder, oracle_files[i - 1])
        curr_path = os.path.join(oracle_folder, oracle_files[i])

        recall = evaluate_recall(curr_path, prev_path)  # how well curr is approximated by prev
        rbo_score = evaluate_rbo(curr_path, prev_path)

        write_metric_to_file(recall_log_file, i, recall)
        write_metric_to_file(rbo_log_file, i, rbo_score)



def run_all_datasets_shift(dataset_configs):
    for dataset_name, config in dataset_configs.items():
        print(f"\n\n### Evaluating snapshot shift on dataset: {dataset_name} ###")
        evaluate_snapshot_shift(
            oracle_folder=config["oracle_folder"],
            output_folder=config["base_output_folder"]
        )

if __name__ == "__main__":
    dataset_configs = {
        "as_733": {
            "oracle_folder": "/home/nikolabulat/sample/Tonic/oracles/as_733/nodes_practical_real",
            "base_output_folder": "/home/nikolabulat/Snapshot_Update/Tonic/preliminary_analysis/outputs/as_733_one_before_predictor"
        },
        "caida": {
            "oracle_folder": "/home/nikolabulat/sample/Tonic/oracles/as_caida_122/nodes_practical_real",
            "base_output_folder": "/home/nikolabulat/Snapshot_Update/Tonic/preliminary_analysis/outputs/as_caida_122_one_before_predictor"
        },
        "oregon1": {
            "oracle_folder": "/home/nikolabulat/sample/Tonic/oracles/oregon/nodes_practical_real",
            "base_output_folder": "/home/nikolabulat/Snapshot_Update/Tonic/preliminary_analysis/outputs/oregon1_one_before_predictor"
        }
    }

    run_all_datasets_shift(dataset_configs)
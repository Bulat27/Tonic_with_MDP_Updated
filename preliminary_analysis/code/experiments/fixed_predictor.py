import os
from evaluation import evaluate_recall, evaluate_rbo, evaluate_linear_ndcg
from utils import load_node_frequencies_txt
from utils import write_metric_to_file

def evaluate_fixed_predictor_against_oracles(oracle_folder, fixed_predictor_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    oracle_files = sorted([f for f in os.listdir(oracle_folder) if os.path.isfile(os.path.join(oracle_folder, f))])

    run_output_dir = os.path.join(output_folder, "run")
    os.makedirs(run_output_dir, exist_ok=True)

    fixed_output_csv = os.path.join(run_output_dir, "fixed_top_nodes.csv")

    if not os.path.exists(fixed_output_csv):
        fixed_predictor = load_node_frequencies_txt(fixed_predictor_path)
        with open(fixed_output_csv, 'w') as f:
            f.write("Node,Degree\n")
            for node_id, freq in fixed_predictor:
                f.write(f"{node_id},{freq}\n")
    else:
        print("Fixed predictor file already exists, skipping creation.")

    for idx, oracle_file in enumerate(oracle_files):
        gt_path = os.path.join(oracle_folder, oracle_file)

        recall = evaluate_recall(gt_path, fixed_output_csv)
        rbo_score = evaluate_rbo(gt_path, fixed_output_csv)
        # ndcg_score = evaluate_linear_ndcg(gt_path, fixed_output_csv)

        recall_log_file = os.path.join(run_output_dir, "recall_values.txt")
        rbo_log_file = os.path.join(run_output_dir, "rbo.txt")
        # ndcg_log_file = os.path.join(run_output_dir, "ndcg_linear.txt")

        write_metric_to_file(recall_log_file, idx, recall)
        # write_metric_to_file(ndcg_log_file, idx, ndcg_score)
        write_metric_to_file(rbo_log_file, idx, rbo_score)

def run_all_datasets_fixed(dataset_configs):
    for dataset_name, config in dataset_configs.items():
        print(f"\n\n### Evaluating on dataset: {dataset_name} ###")
        evaluate_fixed_predictor_against_oracles(
            oracle_folder=config["oracle_folder"],
            fixed_predictor_path=config["fixed_predictor_path"],
            output_folder=config["base_output_folder"]
        )

if __name__ == "__main__":

    dataset_configs = {

        "as_733": {
            "oracle_folder": "/home/nikolabulat/sample/Tonic/oracles/as_733/nodes_practical_real",
            "base_output_folder": "/home/nikolabulat/Snapshot_Update/Tonic/preliminary_analysis/outputs/as_733_fixed_predictor",
            "fixed_predictor_path": "/home/nikolabulat/sample/Tonic/oracles/as_733/nodes_practical_real/oracle_nodes_practical_preprocessed_as19971108.txt"
        },
        "caida": {
            "oracle_folder": "/home/nikolabulat/sample/Tonic/oracles/as_caida_122/nodes_practical_real",
            "base_output_folder": "/home/nikolabulat/Snapshot_Update/Tonic/preliminary_analysis/outputs/as_caida_122_fixed_predictor",
            "fixed_predictor_path": "/home/nikolabulat/sample/Tonic/oracles/as_caida_122/nodes_practical_real/oracle_nodes_practical_preprocessed_as-caida20040105.txt"
        },
        "oregon1": {
            "oracle_folder": "/home/nikolabulat/sample/Tonic/oracles/oregon/nodes_practical_real",
            "base_output_folder": "/home/nikolabulat/Snapshot_Update/Tonic/preliminary_analysis/outputs/oregon1_fixed_predictor",
            "fixed_predictor_path": "/home/nikolabulat/sample/Tonic/oracles/oregon/nodes_practical_real/oracle_nodes_practical_preprocessed_oregon1_010331.txt"
        }
    }

    run_all_datasets_fixed(dataset_configs)
import os
import argparse
from evaluation import evaluate_recall, evaluate_rbo
from utils import write_metric_to_file

def parse_args():
    parser = argparse.ArgumentParser(description="Evaluate Previous Snapshot MinDegreePredictor against all MinDegreePredictors")
    parser.add_argument("-o", "--oracle_folder", required=True, help="Folder containing MinDegreePredictor files")
    parser.add_argument("-n", "--name", required=True, help="Output name")
    return parser.parse_args()

def main():
    args = parse_args()

    OUTPUT_ROOT = f"output/MDPredictorSimilarityExperiments/{args.name}"
    os.makedirs(OUTPUT_ROOT, exist_ok=True)

    oracle_files = sorted([ f for f in os.listdir(args.oracle_folder) if os.path.isfile(os.path.join(args.oracle_folder, f)) and f.endswith(".txt")])

    if not oracle_files:
        raise ValueError("No oracle files found in the specified folder.")

    run_output_dir = os.path.join(OUTPUT_ROOT, "run")
    os.makedirs(run_output_dir, exist_ok=True)

    recall_log_file = os.path.join(run_output_dir, "recall.txt")
    rbo_log_file = os.path.join(run_output_dir, "rbo.txt")
    csv_path = os.path.join(OUTPUT_ROOT, "previous_snapshot_predictor_results.csv")

    with open(csv_path, "w") as csv_file:
        csv_file.write("Algo,RBO,Recall\n")

        for i in range(1, len(oracle_files)):
            prev_path = os.path.join(args.oracle_folder, oracle_files[i - 1])
            curr_path = os.path.join(args.oracle_folder, oracle_files[i])

            recall = evaluate_recall(curr_path, prev_path)
            rbo_score = evaluate_rbo(curr_path, prev_path)

            write_metric_to_file(recall_log_file, i, recall)
            write_metric_to_file(rbo_log_file, i, rbo_score)

            csv_file.write(f"Previous Snapshot MDP,{rbo_score:.6f},{recall:.6f}\n")

if __name__ == "__main__":
    main()
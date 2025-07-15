import os
import argparse
from evaluation import evaluate_recall, evaluate_rbo
from utils import write_metric_to_file

def parse_args():
    """
    Parses command-line arguments for evaluating the similarity between
    MinDegreePredictors across graph snapshots. Similarity (RBO) is calculated between the MinDegreePredictor
    maps of the current and the first snapshot.

    Returns:
        argparse.Namespace: Parsed arguments with oracle folder path and output name.
    """
    parser = argparse.ArgumentParser(description="Evaluate Fixed MinDegreePredictor (first snapshot) against all MinDegreePredictors")
    parser.add_argument("-o", "--oracle_min_degree_folder", required=True, help="Folder containing MinDegreePredictor files")
    parser.add_argument("-n", "--name", required=True, help="Output name")
    return parser.parse_args()

def main():
    """
    Evaluates the similarity between MinDegreePredictors across consecutive graph snapshots.
    Similarity (measured using RBO) is calculated between the MinDegreePredictor
    maps of the current and the first snapshot.

    For each snapshot (excluding the first):
    - It compares the MinDegreePredictor from snapshot 1 (the first snapshot) to snapshot i (current)
    - Computes Recall and RBO similarity between the two
    - Saves per-snapshot metrics to text files
    - Writes a CSV summarizing the full results

    Output:
        - recall.txt and rbo.txt in a `run/` subfolder
        - summary CSV at: output/MDPredictorSimilarityExperiments/{name}/previous_snapshot_predictor_results.csv
    """
    args = parse_args()

    OUTPUT_ROOT = f"output/MDPredictorSimilarityExperiments/{args.name}"
    os.makedirs(OUTPUT_ROOT, exist_ok=True)

    oracle_files = sorted([f for f in os.listdir(args.oracle_min_degree_folder) if os.path.isfile(os.path.join(args.oracle_min_degree_folder, f))])

    if not oracle_files:
        raise ValueError("No oracle files found in the specified folder.")

    fixed_predictor_path = os.path.join(args.oracle_min_degree_folder, oracle_files[0])

    run_output_dir = os.path.join(OUTPUT_ROOT, "run")
    os.makedirs(run_output_dir, exist_ok=True)

    final_csv_path = os.path.join(OUTPUT_ROOT, "first_snapshot_predictor_results.csv")
    with open(final_csv_path, "w") as out_csv:
        out_csv.write("Algo,RBO,Recall\n")

        for idx, oracle_file in enumerate(oracle_files):
            gt_path = os.path.join(args.oracle_min_degree_folder, oracle_file)

            recall = evaluate_recall(gt_path, fixed_predictor_path)
            rbo_score = evaluate_rbo(gt_path, fixed_predictor_path)

            # Write individual metrics to .txt
            recall_log_file = os.path.join(run_output_dir, "recall.txt")
            rbo_log_file = os.path.join(run_output_dir, "rbo.txt")
            write_metric_to_file(recall_log_file, idx, recall)
            write_metric_to_file(rbo_log_file, idx, rbo_score)

            # Append CSV containg all the results
            out_csv.write(f"First Snapshot MDP,{rbo_score:.6f},{recall:.6f}\n")

if __name__ == "__main__":
    main()
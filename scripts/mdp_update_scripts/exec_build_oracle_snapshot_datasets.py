import os
import argparse
import subprocess

def parse_args():
    """
    Parses command-line arguments for generating snapshot oracles using the BuildOracle binary.

    Returns:
        argparse.Namespace: Parsed arguments including dataset path, oracle parameters, and output folder.
    """
    parser = argparse.ArgumentParser(description="Run BuildOracle on graph snapshots to generate oracle files")
    parser.add_argument('-d', '--dataset_folder', required=True, help='Dataset folder containing preprocessed snapshot files')
    parser.add_argument('-t', '--oracle_type', required=True, choices=['Exact', 'noWR', 'Node'], help='Type of oracle to build')
    parser.add_argument('-p', '--percentage_retain', required=True, help='Fraction of top-heavy elements to retain in the oracle')
    parser.add_argument('-x', '--prefix', required=True, help='Prefix for naming the output oracle files')
    parser.add_argument('-o', '--output_folder', required=True, help='Folder to save the oracle files')
    return parser.parse_args()

def main():
    args = parse_args()

    FILE_BUILD_ORACLE = "./code/Tonic-build/BuildOracle"
    os.makedirs(args.output_folder, exist_ok=True)

    dataset_files = sorted([f for f in os.listdir(args.dataset_folder) if os.path.isfile(os.path.join(args.dataset_folder, f))])

    for dataset_filename in dataset_files:
        dataset_path = os.path.join(args.dataset_folder, dataset_filename)

        # "preprocessed" will be the prefix if exec_preprocess_snapshot_datasets.py was used to preprocess the raw snapshot files
        if dataset_filename.startswith("preprocessed_"):
            suffix = dataset_filename[len("preprocessed_"):]
        else:
            suffix = dataset_filename

        # Ensure the prefix ends with an underscore
        prefix = args.prefix if args.prefix.endswith('_') else args.prefix + '_'
        oracle_name = prefix + suffix

        output_path = os.path.join(args.output_folder, oracle_name)

        print(f"\nRunning BuildOracle on: {dataset_filename}")

        subprocess.run([
            FILE_BUILD_ORACLE,
            dataset_path,
            args.oracle_type,
            args.percentage_retain,
            output_path
        ], check=True)

        print(f"Oracle written to: {oracle_name}")

if __name__ == "__main__":
    main()
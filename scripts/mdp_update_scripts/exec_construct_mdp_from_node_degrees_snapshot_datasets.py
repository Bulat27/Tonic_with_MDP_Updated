import os
import argparse

def parse_args():
    """
    Parses command-line arguments for truncating precomputed node oracles based on nbar values. 
    The truncated files represent MinDegreePredictors for each snapshot.

    Returns:
        argparse.Namespace: Parsed arguments including oracle input folder, nbar file, and output folder.
    """
    parser = argparse.ArgumentParser(description="Truncate precomputed node oracles with all node-degree pairs, based on provided nbar values")
    parser.add_argument('-i', '--input_folder', required=True, help='Folder containing precomputed node oracles with all node-degree pairs')
    parser.add_argument('-b', '--nbar_file', required=True, help='Path to .txt file with one nbar value per snapshot')
    parser.add_argument('-o', '--output_folder', required=True, help='Folder to save truncated oracle files')
    return parser.parse_args()

def main():
    args = parse_args()
    os.makedirs(args.output_folder, exist_ok=True)

    oracle_files = sorted([f for f in os.listdir(args.input_folder) if os.path.isfile(os.path.join(args.input_folder, f))])

    with open(args.nbar_file, "r") as f:
        nbar_values = [int(line.strip()) for line in f if line.strip()]

    if len(oracle_files) != len(nbar_values):
        raise ValueError(f"Mismatch between number of oracle files ({len(oracle_files)}) "
                         f"and number of nbar values ({len(nbar_values)}).")

    for oracle_filename, nbar in zip(oracle_files, nbar_values):
        oracle_path = os.path.join(args.input_folder, oracle_filename)
        output_path = os.path.join(args.output_folder, oracle_filename)

        with open(oracle_path, 'r') as f:
            lines = f.readlines()

        with open(output_path, 'w') as f:
            f.writelines(lines[:nbar])

        print(f"Truncated oracle written to: {output_path} (top {nbar} nodes)")

if __name__ == "__main__":
    main()
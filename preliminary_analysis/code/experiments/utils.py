import os

def write_metric_to_file(filepath, snapshot_idx, value):
    with open(filepath, "a") as f:
        f.write(f"{snapshot_idx} {value:.6f}\n")

def load_node_frequencies_txt(filename):
    results = []
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                node_id = int(parts[0])
                freq = int(parts[1])
                results.append((node_id, freq))
    return sorted(results, key=lambda x: -x[1])


def load_node_frequencies_csv(filename):
    results = []
    with open(filename, 'r') as f:
        next(f)  # skip header
        for line in f:
            parts = line.strip().split(',')
            if len(parts) == 2:
                node_id = int(parts[0])
                freq = int(parts[1])
                results.append((node_id, freq))
    return sorted(results, key=lambda x: -x[1])

def load_node_frequencies(filename):
    ext = os.path.splitext(filename)[1].lower()
    if ext == ".csv":
        return load_node_frequencies_csv(filename)
    elif ext == ".txt":
        return load_node_frequencies_txt(filename)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")

def assign_rank_values_batch(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    # List all .txt files in the input folder (sorted for consistent order)
    txt_files = sorted([
        f for f in os.listdir(input_folder)
        if f.endswith(".txt") and os.path.isfile(os.path.join(input_folder, f))
    ])

    for filename in txt_files:
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        # Process individual file
        node_degrees = []
        with open(input_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 2:
                    node_id = int(parts[0])
                    degree = int(parts[1])
                    node_degrees.append((node_id, degree))

        # Extract and sort unique degrees descending
        unique_degrees = sorted(set(degree for _, degree in node_degrees), reverse=True)

        # Map degree to rank
        degree_to_rank = {deg: rank for rank, deg in enumerate(unique_degrees)}
        max_rank = len(unique_degrees) - 1

        # Map node_id to assigned value (rank points)
        node_to_value = {
            node_id: max_rank - degree_to_rank[degree]
            for node_id, degree in node_degrees
        }

        # Write output
        with open(output_path, 'w') as f_out:
            for node_id, value in node_to_value.items():
                f_out.write(f"{node_id} {value}\n")

        print(f"Processed: {filename}")

# if __name__ == "__main__":
#     input_folder = "/home/nikolabulat/sample/Tonic/oracles/oregon/node_all"
#     output_folder = "/home/nikolabulat/Snapshot_Update/Tonic/preliminary_analysis/auxiliary_input/ranking_point_oracles/oregon"

#     assign_rank_values_batch(input_folder, output_folder)
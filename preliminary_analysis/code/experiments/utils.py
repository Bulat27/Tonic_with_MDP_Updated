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
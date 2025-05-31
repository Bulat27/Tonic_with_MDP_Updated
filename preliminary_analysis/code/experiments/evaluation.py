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


def recall_at_k(true_top_k, predicted_top_k):
    true_ids = set(node for node, _ in true_top_k)
    predicted_ids = set(node for node, _ in predicted_top_k)
    return len(true_ids & predicted_ids) / len(true_ids)


def evaluate_recall(ground_truth_file, estimate_file):
    gt = load_node_frequencies_txt(ground_truth_file)
    est = load_node_frequencies_csv(estimate_file)
    return recall_at_k(gt, est)
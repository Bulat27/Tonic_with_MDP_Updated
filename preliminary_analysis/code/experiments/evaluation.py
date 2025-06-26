import rbo
from utils import load_node_frequencies

def recall_at_k(true_top_k, predicted_top_k):
    true_ids = set(node for node, _ in true_top_k)
    predicted_ids = set(node for node, _ in predicted_top_k)
    return len(true_ids & predicted_ids) / len(true_ids)

def evaluate_recall(ground_truth_file, estimate_file):
    gt = load_node_frequencies(ground_truth_file)
    est = load_node_frequencies(estimate_file)
    return recall_at_k(gt, est)

def evaluate_rbo(ground_truth_file, estimate_file):
    gt = load_node_frequencies(ground_truth_file)
    est = load_node_frequencies(estimate_file)

    true_ids = [node for node, _ in gt]
    predicted_ids = [node for node, _ in est]

    return rbo.RankingSimilarity(true_ids, predicted_ids).rbo(p=1.0)